from __future__ import annotations

import asyncio
import copyreg
import dataclasses
import time
import weakref
from collections import defaultdict
from collections.abc import Callable, Iterable, Iterator, Mapping, MutableMapping
from contextlib import contextmanager
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, Literal, TypeVar

from typing_extensions import dataclass_transform

from . import core
from .logging import log

if TYPE_CHECKING:
    from _typeshed import DataclassInstance, IdentityFunction

MAX_PROPAGATION_TIME = 0.01

propagation_visited: ContextVar[set[tuple[int, tuple[str, ...]]] | None] = \
    ContextVar('propagation_visited', default=None)

bindings: defaultdict[
    tuple[int, tuple[str, ...]],
    list[tuple[Any, Any, tuple[str, ...], Callable[[Any], Any] | None]]
] = defaultdict(list)
bindable_properties: weakref.WeakValueDictionary[tuple[int, tuple[str, ...]], Any] = weakref.WeakValueDictionary()
active_links: list[tuple[Any, tuple[str, ...], Any, tuple[str, ...], Callable[[Any], Any] | None]] = []
_active_links_added = asyncio.Event()

TC = TypeVar('TC', bound=type)
T = TypeVar('T')

_MISSING = object()


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
    bindings[(id(self_obj), self_name_tuple)].append((self_obj, other_obj, other_name_tuple, forward))
    if (id(self_obj), self_name_tuple) not in bindable_properties:
        active_links.append((self_obj, self_name_tuple, other_obj, other_name_tuple, forward))
        _active_links_added.set()
    _propagate(self_obj, self_name_tuple)


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
    bindings[(id(other_obj), other_name_tuple)].append((other_obj, self_obj, self_name_tuple, backward))
    if (id(other_obj), other_name_tuple) not in bindable_properties:
        active_links.append((other_obj, other_name_tuple, self_obj, self_name_tuple, backward))
        _active_links_added.set()
    _propagate(other_obj, other_name_tuple)


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
        # PROTOTYPE: reactive read hook. Skip while propagating (those reads are the binding system's
        # own bookkeeping, not user dependencies) and when no computation is collecting.
        if owner is not None and propagation_visited.get() is None:
            computation = _active_computation.get()
            if computation is not None:
                name = (self.name,)
                dep = (id(owner), name)
                producer = _producers.get(dep)
                if producer is not None and producer is not computation:
                    _pull_readers.append((computation, dep))  # our fresh read of exactly this dep is in flight
                    try:
                        _ensure_current(producer)  # pull a dirty producer up-to-date before it is read
                    finally:
                        _pull_readers.pop()
                _track_read(owner, name)  # dependency capture for computed()/effect()
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
        _notify_subscribers(owner, (self.name,))  # PROTOTYPE: settle reactive computed()/effect() first,
        _propagate(owner, (self.name,))  # so legacy bindings that read a derived value propagate it fresh
        if value_changed and self._change_handler is not None:
            self._change_handler(owner, value)


# =============================================================================
# PROTOTYPE: reactive layer (computed / effect) on top of BindableProperty
# -----------------------------------------------------------------------------
# This is a proof-of-concept for zauberzeug/nicegui#4758, NOT a finished API.
# It shows that `Computed` and `Effect` can be built directly on the existing
# BindableProperty read/write hooks, with automatic dependency tracking, and no
# 0.1 s refresh loop. Known open questions are documented in the discussion.
# =============================================================================

Dependency = tuple[int, tuple[str, ...]]

_MAX_FLUSH_ITERATIONS = 1000

_active_computation: ContextVar[_Computation | None] = ContextVar('active_computation', default=None)
_subscribers: defaultdict[Dependency, weakref.WeakSet[_Computation]] = defaultdict(weakref.WeakSet)
_producers: weakref.WeakValueDictionary[Dependency, _Computation] = weakref.WeakValueDictionary()
_pending: set[_Computation] = set()
# (computation, dep) pairs currently pulling that exact producer up-to-date as a fresh read:
_pull_readers: list[tuple[_Computation, Dependency]] = []
_batch_depth = 0
_flushing = False


def _track_read(owner: Any, name: tuple[str, ...]) -> None:
    """Record that the currently-running computation read this bindable property, and subscribe now.

    Subscribing at read time (not at end of run) means a write to a dependency *during* the same run
    -- e.g. an effect that writes state it just read -- still notifies the computation.
    """
    computation = _active_computation.get()
    if computation is not None:
        dep = (id(owner), name)
        computation._collecting.add(dep)  # pylint: disable=protected-access
        _subscribers[dep].add(computation)


def _notify_subscribers(owner: Any, name: tuple[str, ...]) -> None:
    """Mark every computation that read this property dirty, then flush.

    Marking is cheap and synchronous; actual recomputation is deferred to :func:`_flush` so a single
    logical change settles the whole graph once, in dependency order -- rather than re-running
    dependents eagerly and depth-first, which double-runs diamonds and lets effects observe
    half-updated state.
    """
    dep = (id(owner), name)
    subscribers = _subscribers.get(dep)
    if not subscribers:
        if subscribers is not None:
            del _subscribers[dep]  # reap a key left empty by a garbage-collected computation
        return
    for computation in list(subscribers):
        if (computation, dep) in _pull_readers:
            continue  # it is pulling THIS dep as a fresh read in this very run: no re-enqueue needed
        computation._dirty = True  # pylint: disable=protected-access
        _pending.add(computation)
    _flush()


def _unsubscribe(dep: Dependency, computation: _Computation) -> None:
    """Drop a computation's subscription, pruning the entry entirely when its last subscriber leaves.

    (This keeps churn -- re-subscription on every run, plus ``dispose()`` -- from growing
    ``_subscribers`` without bound. Computations garbage-collected *without* ``dispose()`` still leave
    an empty entry behind; reaping those is part of the lifecycle work a production version must add.)
    """
    subscribers = _subscribers.get(dep)
    if subscribers is not None:
        subscribers.discard(computation)
        if not subscribers:
            del _subscribers[dep]


class _Computation:
    """Runs a function while recording which bindable properties it reads, then re-runs on change.

    Dependencies are re-captured on every run, so branching reactive code subscribes only to the
    properties it actually touched this time (dynamic dependency tracking).
    """

    def __init__(self, fn: Callable[[], Any]) -> None:
        self._fn = fn
        self._deps: set[Dependency] = set()
        self._collecting: set[Dependency] = set()
        self._dirty = False
        self._running = False
        self._run()

    def _run(self) -> Any:
        self._collecting = set()
        self._dirty = False
        self._running = True
        token = _active_computation.set(self)
        try:
            result = self._fn()
        finally:
            _active_computation.reset(token)
            self._running = False
            # Reconcile deps even if fn() raised, so dispose() can unsubscribe what was read before the error
            # (fresh deps are subscribed incrementally in _track_read; drop ones not read this run).
            for stale in self._deps - self._collecting:
                _unsubscribe(stale, self)
            self._deps = self._collecting
        if self._dirty:  # re-invalidated during our own run (e.g. we wrote a dependency we had read)
            _pending.add(self)
            _flush()  # converge; a genuinely unbounded feedback loop trips the _flush cycle guard
        return result

    def dispose(self) -> None:
        """Unsubscribe from all dependencies so this computation stops re-running."""
        for dep in self._deps:
            _unsubscribe(dep, self)
        self._deps = set()
        self._dirty = False
        _pending.discard(self)


def _ensure_current(computation: _Computation) -> None:
    """Recompute a dirty computation now. Used by the flush loop and by pull-on-read in ``__get__``."""
    _pending.discard(computation)
    if computation._dirty and not computation._running:  # pylint: disable=protected-access
        computation._run()  # pylint: disable=protected-access


def _flush() -> None:
    """Recompute all pending computations, once each, in dependency order.

    Ordering falls out of two mechanisms rather than an explicit topological sort: recomputing a
    producer re-enters :func:`_notify_subscribers`, enqueueing its dependents; and a dependent that
    happens to run first pulls any still-dirty producer it reads up-to-date via
    :meth:`BindableProperty.__get__` before using it. So a diamond's sink recomputes exactly once,
    after both sources have settled -- never on a half-updated intermediate.
    """
    global _flushing  # pylint: disable=global-statement # noqa: PLW0603
    if _flushing or _batch_depth:
        return
    _flushing = True
    try:
        iterations = 0
        while _pending:
            iterations += 1
            if iterations > _MAX_FLUSH_ITERATIONS:
                _pending.clear()  # drop the poisoned graph state so a later unrelated write isn't re-poisoned
                raise RuntimeError('Reactive cycle detected: the computed()/effect() graph did not '
                                   'settle. A computation likely depends (transitively) on its own output.')
            _ensure_current(next(iter(_pending)))
    finally:
        _flushing = False


@contextmanager
def batch() -> Iterator[None]:
    """Coalesce multiple bindable-property writes into a single reactive flush (*PROTOTYPE*).

    Without a batch, every write settles the reactive graph immediately, so reads see fresh values
    synchronously. Inside a batch, writes only mark dependents dirty; the flush runs once when the
    outermost batch exits, so a dependent recomputes at most once regardless of how many of its
    sources changed::

        with binding.batch():
            order.price = 5
            order.quantity = 9   # a subtotal computed from both recomputes once, not twice
    """
    global _batch_depth  # pylint: disable=global-statement # noqa: PLW0603
    _batch_depth += 1
    try:
        yield
    finally:
        _batch_depth -= 1
        if _batch_depth == 0:
            _flush()


class Computed:
    """A derived value that recomputes automatically when any bindable property it reads changes.

    The result is exposed as a bindable ``value``, so it plugs straight into ``bind_*`` and elements::

        total = binding.computed(lambda: state.price * state.qty)
        ui.label().bind_text_from(total, 'value')
    """
    value = BindableProperty()

    def __init__(self, fn: Callable[[], Any]) -> None:
        self._fn = fn
        self._computation = _Computation(lambda: setattr(self, 'value', self._fn()))
        _producers[(id(self), ('value',))] = self._computation  # so dependents can pull us up-to-date

    def dispose(self) -> None:
        """Stop recomputing (dispose the underlying computation)."""
        _producers.pop((id(self), ('value',)), None)
        self._computation.dispose()


class Effect:
    """Runs a side-effecting function whenever any bindable property it reads changes.

    Keep a reference to the returned ``Effect`` for as long as you need it; call ``dispose()``
    (e.g. on client disconnect) to stop it and release its subscriptions.
    """

    def __init__(self, fn: Callable[[], Any]) -> None:
        self._computation = _Computation(fn)

    def dispose(self) -> None:
        """Stop running and release all dependency subscriptions."""
        self._computation.dispose()


def computed(fn: Callable[[], T]) -> Computed:
    """Create a `Computed` derived value from a function of other bindable properties (*PROTOTYPE*)."""
    return Computed(fn)


def effect(fn: Callable[[], Any]) -> Effect:
    """Create an `Effect` that re-runs whenever the bindable properties it reads change (*PROTOTYPE*)."""
    return Effect(fn)


def remove(objects: Iterable[Any]) -> None:
    """Remove all bindings that involve the given objects.

    :param objects: The objects to remove.
    """
    object_ids = set(map(id, objects))
    active_links[:] = [
        (source_obj, source_name, target_obj, target_name, transform)
        for source_obj, source_name, target_obj, target_name, transform in active_links
        if id(source_obj) not in object_ids and id(target_obj) not in object_ids
    ]
    for key, binding_list in list(bindings.items()):
        binding_list[:] = [
            (source_obj, target_obj, target_name, transform)
            for source_obj, target_obj, target_name, transform in binding_list
            if id(source_obj) not in object_ids and id(target_obj) not in object_ids
        ]
        if not binding_list:
            del bindings[key]
    for obj_id, name in list(bindable_properties):
        if obj_id in object_ids:
            del bindable_properties[(obj_id, name)]


def reset() -> None:
    """Clear all bindings.

    This function is intended for testing purposes only.
    """
    global _batch_depth, _flushing  # pylint: disable=global-statement # noqa: PLW0603
    bindings.clear()
    bindable_properties.clear()
    active_links.clear()
    _subscribers.clear()  # PROTOTYPE: also drop reactive computed()/effect() state
    _producers.clear()
    _pending.clear()
    _pull_readers.clear()
    _batch_depth = 0
    _flushing = False


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
