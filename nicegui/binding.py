from __future__ import annotations

import asyncio
import copyreg
import dataclasses
import time
import weakref
from collections import defaultdict
from collections.abc import Callable, Iterable, Iterator, Mapping, MutableMapping
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, Literal, TypeVar

from typing_extensions import dataclass_transform

from . import core
from .logging import log

if TYPE_CHECKING:
    from _typeshed import DataclassInstance, IdentityFunction

ObjectId = int
NamePath = tuple[str, ...]
NameBucket = NamePath | set[NamePath]
BindingKey = tuple[ObjectId, NamePath]
BindingKeyBucket = BindingKey | set[BindingKey]
Transform = Callable[[Any], Any] | None
Binding = tuple[Any, Any, NamePath, Transform]
ActiveLink = tuple[Any, NamePath, Any, NamePath, Transform]
BindableEntry = tuple[weakref.ref[Any], NameBucket]


class _BindablePropertyRegistry:
    """Weak bindable-property registry keyed by object ID with name-path buckets.

    Most bindable objects expose one bindable property, so the common case stores a single name path and upgrades to a
    set only when the same object has multiple bindable properties.
    """

    def __init__(self) -> None:
        self._entries_by_object_id: dict[ObjectId, BindableEntry] = {}

    def _discard_object_id(self, obj_id: ObjectId) -> None:
        self._entries_by_object_id.pop(obj_id, None)

    def __setitem__(self, key: BindingKey, obj: Any) -> None:
        obj_id, name_path = key
        entry = self._entries_by_object_id.get(obj_id)
        if entry is None:
            def discard(_: weakref.ref[Any], obj_id: ObjectId = obj_id) -> None:
                self._discard_object_id(obj_id)
            self._entries_by_object_id[obj_id] = (weakref.ref(obj, discard), name_path)
            return
        ref, name_bucket = entry
        if isinstance(name_bucket, set):
            name_bucket.add(name_path)
        elif name_bucket != name_path:
            self._entries_by_object_id[obj_id] = (ref, {name_bucket, name_path})

    def contains_key(self, key: BindingKey) -> bool:
        """Return whether a validated binding key is registered."""
        obj_id, name_path = key
        entry = self._entries_by_object_id.get(obj_id)
        if entry is None:
            return False
        ref, name_bucket = entry
        if ref() is None:
            self._discard_object_id(obj_id)
            return False
        return name_path in name_bucket if isinstance(name_bucket, set) else name_bucket == name_path

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, tuple) or len(key) != 2:
            return False
        return self.contains_key(key)  # type: ignore[arg-type]

    def __iter__(self) -> Iterator[BindingKey]:
        # Copy before iterating because weakref callbacks can mutate this dictionary.
        for obj_id, (ref, name_bucket) in list(self._entries_by_object_id.items()):
            if ref() is None:
                self._discard_object_id(obj_id)
                continue
            if isinstance(name_bucket, set):
                for name_path in name_bucket:
                    yield obj_id, name_path
            else:
                yield obj_id, name_bucket

    def clear(self) -> None:
        """Remove all registered bindable-property entries."""
        self._entries_by_object_id.clear()

    def discard_object_ids(self, object_ids: Iterable[int]) -> None:
        """Remove registered bindable-property entries for the given object IDs."""
        pop = self._entries_by_object_id.pop
        for obj_id in object_ids:
            pop(obj_id, None)


MAX_PROPAGATION_TIME = 0.01

propagation_visited: ContextVar[set[BindingKey] | None] = \
    ContextVar('propagation_visited', default=None)

bindings: defaultdict[
    BindingKey,
    list[Binding]
] = defaultdict(list)
bindable_properties: _BindablePropertyRegistry = _BindablePropertyRegistry()
active_links: list[ActiveLink] = []
_active_links_added = asyncio.Event()
# Maps object IDs to binding keys that reference them, so remove() avoids scanning all bindings.
_binding_keys_by_object: dict[ObjectId, BindingKeyBucket] = {}

TC = TypeVar('TC', bound=type)
T = TypeVar('T')

_MISSING = object()


def _bucket_add(bucket_dict: dict[Any, Any], key: Any, value: Any) -> None:
    """Add value to a scalar-or-set bucket in a dict.

    Most objects have a single entry, so the common case stores a bare value
    and upgrades to a set only when a second distinct value is added.
    """
    bucket = bucket_dict.get(key)
    if bucket is None:
        bucket_dict[key] = value
    elif isinstance(bucket, set):
        bucket.add(value)
    elif bucket != value:
        bucket_dict[key] = {bucket, value}


def _bucket_discard(bucket_dict: dict[Any, Any], key: Any, value: Any) -> None:
    """Remove value from a scalar-or-set bucket in a dict; delete bucket if empty."""
    bucket = bucket_dict.get(key)
    if bucket is None:
        return
    if not isinstance(bucket, set):
        if bucket == value:
            del bucket_dict[key]
        return
    bucket.discard(value)
    if not bucket:
        del bucket_dict[key]


def _discard_binding_key_from_object_index(obj_id: ObjectId, binding_key: BindingKey) -> None:
    """Remove one binding key from the reverse index used by remove()."""
    _bucket_discard(_binding_keys_by_object, obj_id, binding_key)


def _add_binding_key_to_object_index(obj_id: ObjectId, binding_key: BindingKey) -> None:
    """Add one endpoint reference to the reverse index used by remove()."""
    _bucket_add(_binding_keys_by_object, obj_id, binding_key)


def _index_binding(source_obj: Any, target_obj: Any, binding_key: BindingKey) -> None:
    """Index both endpoints so remove() can find affected binding lists without a full scan."""
    _add_binding_key_to_object_index(id(source_obj), binding_key)
    _add_binding_key_to_object_index(id(target_obj), binding_key)


def _bind_one_way(source_obj: Any, source_name: NamePath, target_obj: Any, target_name: NamePath,
                  transform: Transform) -> None:
    """Register a one-way binding and run its initial propagation."""
    binding_key = (id(source_obj), source_name)
    bindings[binding_key].append((source_obj, target_obj, target_name, transform))
    _index_binding(source_obj, target_obj, binding_key)
    if not bindable_properties.contains_key(binding_key):
        active_links.append((source_obj, source_name, target_obj, target_name, transform))
        _active_links_added.set()
    _propagate(source_obj, source_name)


def _collect_binding_keys_for_objects(object_ids: Iterable[ObjectId]) -> set[BindingKey] | None:
    """Return binding keys whose source or target may reference the given objects."""
    # Stay at None until the first hit so remove() calls for objects with no active
    # bindings ("ghost removals") skip the set allocation and traversal entirely.
    binding_keys: set[BindingKey] | None = None
    get_object_binding_keys = _binding_keys_by_object.get
    for obj_id in object_ids:
        bucket = get_object_binding_keys(obj_id)
        if bucket is None:
            continue
        if binding_keys is None:
            binding_keys = set()
        if isinstance(bucket, set):
            binding_keys.update(bucket)
        else:
            binding_keys.add(bucket)
    return binding_keys


def _remove_active_links_for_objects(removed_object_ids: set[ObjectId]) -> None:
    """Drop polling fallback links that reference any removed object."""
    active_links[:] = [
        (source_obj, source_name, target_obj, target_name, transform)
        for source_obj, source_name, target_obj, target_name, transform in active_links
        if id(source_obj) not in removed_object_ids and id(target_obj) not in removed_object_ids
    ]


def _get_attribute(obj: object | Mapping, name: tuple[str, ...]) -> Any:
    try:
        for key in name:
            obj = obj[key] if isinstance(obj, Mapping) else getattr(obj, key)
    except (KeyError, AttributeError):
        return _MISSING
    return obj


def _set_attribute(obj: object | Mapping, name: tuple[str, ...], value: Any) -> None:
    for key in name[:-1]:
        if isinstance(obj, MutableMapping):
            obj = obj.setdefault(key, {})
        else:
            type_ = obj.__class__.__name__
            obj = getattr(obj, key, _MISSING)
            if obj is _MISSING:
                raise AttributeError(f'Cannot traverse intermediate attribute "{key}" on object of type {type_}. '
                                     'Only dict intermediates are auto-created for missing keys.')
    if isinstance(obj, MutableMapping):
        obj[name[-1]] = value
    else:
        setattr(obj, name[-1], value)


async def refresh_loop() -> None:
    """Refresh all bindings in an endless loop."""
    global _active_links_added  # pylint: disable=global-statement # noqa: PLW0603
    _active_links_added = asyncio.Event()
    await _active_links_added.wait()
    if core.app.config.binding_refresh_interval is None:
        core.app.config.binding_refresh_interval = 0.1
        log.warning('Starting active binding loop even though it was disabled via binding_refresh_interval=None.')
    while True:
        _refresh_step()
        try:
            await asyncio.sleep(core.app.config.binding_refresh_interval)
        except asyncio.CancelledError:
            break


def _refresh_step() -> None:
    t = time.time()
    for link in active_links:
        (source_obj, source_name, target_obj, target_name, transform) = link
        if (source_value := _get_attribute(source_obj, source_name)) is not _MISSING:
            value = transform(source_value) if transform else source_value
            if (target_value := _get_attribute(target_obj, target_name)) is _MISSING or target_value != value:
                _set_attribute(target_obj, target_name, value)
                _propagate(target_obj, target_name)
        del link, source_obj, target_obj  # pylint: disable=modified-iterating-list
    if time.time() - t > MAX_PROPAGATION_TIME:
        log.warning(f'binding propagation for {len(active_links)} active links took {time.time() - t:.3f} s')


def _propagate(source_obj: Any, source_name: tuple[str, ...]) -> None:
    token = propagation_visited.set(set())
    try:
        _propagate_recursively(source_obj, source_name)
    finally:
        propagation_visited.reset(token)


def _propagate_recursively(source_obj: Any, source_name: tuple[str, ...]) -> None:
    visited = propagation_visited.get()
    assert visited is not None, 'propagation_visited is not set'

    source_obj_id = id(source_obj)
    if (source_obj_id, source_name) in visited:
        return
    visited.add((source_obj_id, source_name))

    if (source_value := _get_attribute(source_obj, source_name)) is _MISSING:
        return

    for _, target_obj, target_name, transform in bindings.get((source_obj_id, source_name), []):
        if (id(target_obj), target_name) in visited:
            continue

        target_value = transform(source_value) if transform else source_value
        if (current := _get_attribute(target_obj, target_name)) is _MISSING or current != target_value:
            _set_attribute(target_obj, target_name, target_value)
            _propagate_recursively(target_obj, target_name)


def _check_attribute_exists(obj: Any, name: tuple[str, ...], *, role: Literal['self', 'other']) -> None:
    if _get_attribute(obj, name) is not _MISSING:
        return
    for key in name:
        try:
            obj = obj[key] if isinstance(obj, Mapping) else getattr(obj, key)
        except (KeyError, AttributeError):
            break
    if isinstance(obj, Mapping):
        raise KeyError(
            f'Could not bind non-existing key "{".".join(name)}". '
            f'To allow missing keys (lazy binding), remove {role}_strict=True or add the key before binding.'
        )
    else:
        raise AttributeError(
            f'Could not bind non-existing attribute "{".".join(name)}" on object of type {obj.__class__.__name__}. '
            f'To allow missing attributes (lazy binding), add {role}_strict=False or add the attribute before binding.'
        )


def _check_self_and_other_attribute(self_obj: Any, self_name: tuple[str, ...], other_obj: Any,
                                    other_name: tuple[str, ...],
                                    self_strict: bool | None, other_strict: bool | None) -> None:
    if self_strict or (self_strict is None and not _path_contains_dict(self_obj, self_name)):
        _check_attribute_exists(self_obj, self_name, role='self')
    if other_strict or (other_strict is None and not _path_contains_dict(other_obj, other_name)):
        _check_attribute_exists(other_obj, other_name, role='other')


def bind_to(self_obj: Any, self_name: str | tuple[str, ...], other_obj: Any, other_name: str | tuple[str, ...],
            forward: Callable[[Any], Any] | None = None, *,
            self_strict: bool | None = None, other_strict: bool | None = None) -> None:
    """Bind the property of one object to the property of another object.

    The binding works one way only, from the first object to the second.
    The update happens immediately and whenever a value changes.
    The name parameters also accept a tuple of strings for nested keys (*since version 3.10.0*).

    :param self_obj: The object to bind from.
    :param self_name: The name of the property to bind from.
    :param other_obj: The object to bind to.
    :param other_name: The name of the property to bind to.
    :param forward: A function to apply to the value before applying it (default: identity).
    :param self_strict: Whether to check (and raise) if the first object has the specified property
        (default: None, performs a check if the object is not a dictionary, *added in version 3.0.0*).
    :param other_strict: Whether to check (and raise) if the second object has the specified property
        (default: None, performs a check if the object is not a dictionary, *added in version 3.0.0*).
    """
    self_name_tuple = _normalize_name(self_name)
    other_name_tuple = _normalize_name(other_name)
    _check_self_and_other_attribute(self_obj, self_name_tuple, other_obj, other_name_tuple, self_strict, other_strict)
    _bind_one_way(self_obj, self_name_tuple, other_obj, other_name_tuple, forward)


def bind_from(self_obj: Any, self_name: str | tuple[str, ...], other_obj: Any, other_name: str | tuple[str, ...],
              backward: Callable[[Any], Any] | None = None, *,
              self_strict: bool | None = None, other_strict: bool | None = None) -> None:
    """Bind the property of one object from the property of another object.

    The binding works one way only, from the second object to the first.
    The update happens immediately and whenever a value changes.
    The name parameters also accept a tuple of strings for nested keys (*since version 3.10.0*).

    :param self_obj: The object to bind to.
    :param self_name: The name of the property to bind to.
    :param other_obj: The object to bind from.
    :param other_name: The name of the property to bind from.
    :param backward: A function to apply to the value before applying it (default: identity).
    :param self_strict: Whether to check (and raise) if the first object has the specified property (default: None,
        performs a check if the object is not a dictionary, *added in version 3.0.0*).
    :param other_strict: Whether to check (and raise) if the second object has the specified property (default: None,
        performs a check if the object is not a dictionary, *added in version 3.0.0*).
    """
    self_name_tuple = _normalize_name(self_name)
    other_name_tuple = _normalize_name(other_name)
    _check_self_and_other_attribute(self_obj, self_name_tuple, other_obj, other_name_tuple, self_strict, other_strict)
    _bind_one_way(other_obj, other_name_tuple, self_obj, self_name_tuple, backward)


def bind(self_obj: Any, self_name: str | tuple[str, ...], other_obj: Any, other_name: str | tuple[str, ...], *,
         forward: Callable[[Any], Any] | None = None,
         backward: Callable[[Any], Any] | None = None,
         self_strict: bool | None = None,
         other_strict: bool | None = None) -> None:
    """Bind the property of one object to the property of another object.

    The binding works both ways, from the first object to the second and from the second to the first.
    The update happens immediately and whenever a value changes.
    The backward binding takes precedence for the initial synchronization.
    The name parameters also accept a tuple of strings for nested keys (*since version 3.10.0*).

    :param self_obj: First object to bind.
    :param self_name: The name of the first property to bind.
    :param other_obj: The second object to bind.
    :param other_name: The name of the second property to bind.
    :param forward: A function to apply to the value before applying it to the second object (default: identity).
    :param backward: A function to apply to the value before applying it to the first object (default: identity).
    :param self_strict: Whether to check (and raise) if the first object has the specified property (default: None,
        performs a check if the object is not a dictionary, *added in version 3.0.0*).
    :param other_strict: Whether to check (and raise) if the second object has the specified property (default: None,
        performs a check if the object is not a dictionary, *added in version 3.0.0*).
    """
    self_name_tuple = _normalize_name(self_name)
    other_name_tuple = _normalize_name(other_name)
    _check_self_and_other_attribute(self_obj, self_name_tuple, other_obj, other_name_tuple, self_strict, other_strict)
    bind_from(self_obj, self_name_tuple, other_obj, other_name_tuple,
              backward=backward, self_strict=False, other_strict=False)
    bind_to(self_obj, self_name_tuple, other_obj, other_name_tuple,
            forward=forward, self_strict=False, other_strict=False)


def _normalize_name(name: str | tuple[str, ...]) -> tuple[str, ...]:
    """Convert property name to normalized tuple format."""
    assert name, 'Property name cannot be empty'
    if isinstance(name, tuple):
        assert all(isinstance(key, str) for key in name), 'Property name tuple must contain only strings'
    return name if isinstance(name, tuple) else (name,)


def _path_contains_dict(obj: Any, name: tuple[str, ...]) -> bool:
    """Check if the nested path traverses through any dict/Mapping."""
    for key in name:
        if isinstance(obj, Mapping):
            return True
        if not hasattr(obj, key):
            return False
        obj = getattr(obj, key)
    return False


class BindableProperty:

    def __init__(self, on_change: Callable[..., Any] | None = None) -> None:
        self._change_handler = on_change

    def __set_name__(self, _, name: str) -> None:
        self.name = name  # pylint: disable=attribute-defined-outside-init

    def __get__(self, owner: Any, _=None) -> Any:
        return getattr(owner, '___' + self.name)

    def __set__(self, owner: Any, value: Any) -> None:
        has_attr = hasattr(owner, '___' + self.name)
        if not has_attr:
            _make_copyable(type(owner))
        value_changed = has_attr and getattr(owner, '___' + self.name) != value
        if has_attr and not value_changed:
            return
        setattr(owner, '___' + self.name, value)
        bindable_properties[(id(owner), (self.name,))] = owner
        _propagate(owner, (self.name,))
        if value_changed and self._change_handler is not None:
            self._change_handler(owner, value)


def remove(objects: Iterable[Any]) -> None:
    """Remove all bindings that involve the given objects.

    :param objects: The objects to remove.
    """
    # Keep IDs as a list until membership checks are needed; ghost removals only do dict pop/get by ID.
    removed_object_ids = [id(obj) for obj in objects]
    if not removed_object_ids:
        return

    bindable_properties.discard_object_ids(removed_object_ids)

    affected_binding_keys = _collect_binding_keys_for_objects(removed_object_ids)
    if not affected_binding_keys:
        return

    removed_object_id_set = set(removed_object_ids)
    _remove_active_links_for_objects(removed_object_id_set)

    for key in affected_binding_keys:
        binding_list = bindings.get(key)
        if binding_list is None:
            continue
        source_obj_id = key[0]
        # Binding keys are source IDs; target-only removals only prune entries from the binding list.
        if source_obj_id in removed_object_id_set:
            for _, target_obj, _, _ in binding_list:
                target_obj_id = id(target_obj)
                if target_obj_id not in removed_object_id_set:
                    _discard_binding_key_from_object_index(target_obj_id, key)
            del bindings[key]
            continue
        if len(binding_list) == 1:
            if id(binding_list[0][1]) in removed_object_id_set:
                del bindings[key]
                _discard_binding_key_from_object_index(source_obj_id, key)
            continue
        remaining_bindings = [binding for binding in binding_list if id(binding[1]) not in removed_object_id_set]
        if remaining_bindings:
            binding_list[:] = remaining_bindings
        else:
            del bindings[key]
            _discard_binding_key_from_object_index(source_obj_id, key)

    for obj_id in removed_object_ids:
        _binding_keys_by_object.pop(obj_id, None)


def reset() -> None:
    """Clear all bindings.

    This function is intended for testing purposes only.
    """
    bindings.clear()
    bindable_properties.clear()
    active_links.clear()
    _binding_keys_by_object.clear()


@dataclass_transform()
def bindable_dataclass(cls: TC | None = None, /, *,
                       bindable_fields: Iterable[str] | None = None,
                       **kwargs: Any) -> type[DataclassInstance] | IdentityFunction:
    """A decorator that transforms a class into a dataclass with bindable fields.

    This decorator extends the functionality of ``dataclasses.dataclass`` by making specified fields bindable.
    If ``bindable_fields`` is provided, only the listed fields are made bindable.
    Otherwise, all fields are made bindable by default.

    *Added in version 2.11.0*

    :param cls: class to be transformed into a dataclass
    :param bindable_fields: optional list of field names to make bindable (defaults to all fields)
    :param kwargs: optional keyword arguments to be forwarded to ``dataclasses.dataclass``.
    Usage of ``slots=True`` and ``frozen=True`` are not supported and will raise a ValueError.

    :return: resulting dataclass type
    """
    if cls is None:
        def wrap(cls_):
            return bindable_dataclass(cls_, bindable_fields=bindable_fields, **kwargs)
        return wrap

    for unsupported_option in ('slots', 'frozen'):
        if kwargs.get(unsupported_option):
            raise ValueError(f'`{unsupported_option}=True` is not supported with bindable_dataclass')

    dataclass: type[DataclassInstance] = dataclasses.dataclass(**kwargs)(cls)
    field_names = {field.name for field in dataclasses.fields(dataclass)}
    if bindable_fields is None:
        bindable_fields = field_names
    for field_name in bindable_fields:
        if field_name not in field_names:
            raise ValueError(f'"{field_name}" is not a dataclass field')
        bindable_property = BindableProperty()
        bindable_property.__set_name__(dataclass, field_name)
        setattr(dataclass, field_name, bindable_property)
    return dataclass


def _make_copyable(cls: type[T]) -> None:
    """Tell the copy module to update the ``bindable_properties`` dictionary when an object is copied."""
    if cls in copyreg.dispatch_table:
        return

    def _pickle_function(obj: T) -> tuple[Callable[..., T], tuple[Any, ...]]:
        reduced = obj.__reduce__()
        assert isinstance(reduced, tuple)
        creator = reduced[0]

        def creator_with_hook(*args, **kwargs) -> T:
            copy = creator(*args, **kwargs)
            for attr_name in dir(obj):
                if (id(obj), (attr_name,)) in bindable_properties:
                    bindable_properties[(id(copy), (attr_name,))] = copy
            return copy
        return (creator_with_hook, *reduced[1:])
    copyreg.pickle(cls, _pickle_function)
