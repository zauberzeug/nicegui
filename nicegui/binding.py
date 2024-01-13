import asyncio
import time
from collections import defaultdict
from collections.abc import Mapping
from typing import Any, Callable, DefaultDict, Dict, Iterable, List, Optional, Set, Tuple, Type, Union

from . import core
from .logging import log

MAX_PROPAGATION_TIME = 0.01

bindings: DefaultDict[Tuple[int, str], List] = defaultdict(list)
bindable_properties: Dict[Tuple[int, str], Any] = {}
bindable_properties_names: DefaultDict[int, List] = defaultdict(list)
active_links: List[Tuple[Any, str, Any, str, Callable[[Any], Any]]] = []


def _has_attribute(obj: Union[object, Mapping], name: str) -> Any:
    if isinstance(obj, Mapping):
        return name in obj
    return hasattr(obj, name)


def _get_attribute(obj: Union[object, Mapping], name: str) -> Any:
    if isinstance(obj, Mapping):
        return obj[name]
    return getattr(obj, name)


def _set_attribute(obj: Union[object, Mapping], name: str, value: Any) -> None:
    if isinstance(obj, dict):
        obj[name] = value
    else:
        setattr(obj, name, value)


async def refresh_loop() -> None:
    """Refresh all bindings in an endless loop."""
    while True:
        _refresh_step()
        await asyncio.sleep(core.app.config.binding_refresh_interval)


def _refresh_step() -> None:
    visited: Set[Tuple[int, str]] = set()
    t = time.time()
    for link in active_links:
        (source_obj, source_name, target_obj, target_name, transform) = link
        if _has_attribute(source_obj, source_name):
            value = transform(_get_attribute(source_obj, source_name))
            if not _has_attribute(target_obj, target_name) or _get_attribute(target_obj, target_name) != value:
                _set_attribute(target_obj, target_name, value)
                _propagate(target_obj, target_name, visited)
        del link, source_obj, target_obj  # pylint: disable=modified-iterating-list
    if time.time() - t > MAX_PROPAGATION_TIME:
        log.warning(f'binding propagation for {len(active_links)} active links took {time.time() - t:.3f} s')


def _propagate(source_obj: Any, source_name: str, visited: Optional[Set[Tuple[int, str]]] = None) -> None:
    if visited is None:
        visited = set()
    source_obj_id = id(source_obj)
    if source_obj_id in visited:
        return
    visited.add((source_obj_id, source_name))

    if not _has_attribute(source_obj, source_name):
        return
    source_value = _get_attribute(source_obj, source_name)

    for _, target_obj, target_name, transform in bindings.get((source_obj_id, source_name), []):
        if (id(target_obj), target_name) in visited:
            continue

        target_value = transform(source_value)
        if not _has_attribute(target_obj, target_name) or _get_attribute(target_obj, target_name) != target_value:
            _set_attribute(target_obj, target_name, target_value)
            _propagate(target_obj, target_name, visited)


def bind_to(self_obj: Any, self_name: str, other_obj: Any, other_name: str, forward: Callable[[Any], Any]) -> None:
    """Bind the property of one object to the property of another object.

    The binding works one way only, from the first object to the second.
    The update happens immediately and whenever a value changes.

    :param self_obj: The object to bind from.
    :param self_name: The name of the property to bind from.
    :param other_obj: The object to bind to.
    :param other_name: The name of the property to bind to.
    :param forward: A function to apply to the value before applying it.
    """
    bindings[(id(self_obj), self_name)].append((self_obj, other_obj, other_name, forward))
    if (id(self_obj), self_name) not in bindable_properties:
        active_links.append((self_obj, self_name, other_obj, other_name, forward))
    _propagate(self_obj, self_name)


def bind_from(self_obj: Any, self_name: str, other_obj: Any, other_name: str, backward: Callable[[Any], Any]) -> None:
    """Bind the property of one object from the property of another object.

    The binding works one way only, from the second object to the first.
    The update happens immediately and whenever a value changes.

    :param self_obj: The object to bind to.
    :param self_name: The name of the property to bind to.
    :param other_obj: The object to bind from.
    :param other_name: The name of the property to bind from.
    :param backward: A function to apply to the value before applying it.
    """
    bindings[(id(other_obj), other_name)].append((other_obj, self_obj, self_name, backward))
    if (id(other_obj), other_name) not in bindable_properties:
        active_links.append((other_obj, other_name, self_obj, self_name, backward))
    _propagate(other_obj, other_name)


def bind(self_obj: Any, self_name: str, other_obj: Any, other_name: str, *,
         forward: Callable[[Any], Any] = lambda x: x, backward: Callable[[Any], Any] = lambda x: x) -> None:
    """Bind the property of one object to the property of another object.

    The binding works both ways, from the first object to the second and from the second to the first.
    The update happens immediately and whenever a value changes.
    The backward binding takes precedence for the initial synchronization.

    :param self_obj: First object to bind.
    :param self_name: The name of the first property to bind.
    :param other_obj: The second object to bind.
    :param other_name: The name of the second property to bind.
    :param forward: A function to apply to the value before applying it to the second object.
    :param backward: A function to apply to the value before applying it to the first object.
    """
    bind_from(self_obj, self_name, other_obj, other_name, backward=backward)
    bind_to(self_obj, self_name, other_obj, other_name, forward=forward)


class BindableProperty:

    def __init__(self, on_change: Optional[Callable[..., Any]] = None) -> None:
        self._change_handler = on_change

    def __set_name__(self, _, name: str) -> None:
        self.name = name  # pylint: disable=attribute-defined-outside-init

    def __get__(self, owner: Any, _=None) -> Any:
        return getattr(owner, '___' + self.name)

    def __set__(self, owner: Any, value: Any) -> None:
        has_attr = hasattr(owner, '___' + self.name)
        value_changed = has_attr and getattr(owner, '___' + self.name) != value
        if has_attr and not value_changed:
            return
        setattr(owner, '___' + self.name, value)
        bindable_properties[(id(owner), self.name)] = owner
        bindable_properties_names[id(owner)].append(self.name)
        _propagate(owner, self.name)
        if value_changed and self._change_handler is not None:
            self._change_handler(owner, value)


def remove(objects: Iterable[Any], type_: Type) -> None:
    """Remove all bindings that involve the given objects.

    The ``type_`` argument is as a quick pre-filter.

    :param objects: The objects to remove.
    :param type_: The type of the objects to remove.
    """
    active_links_copy = active_links
    active_links[:] = [
        (source_obj, source_name, target_obj, target_name, transform)
        for source_obj, source_name, target_obj, target_name, transform in active_links_copy
        if not (isinstance(source_obj, type_) and source_obj in objects or
                isinstance(target_obj, type_) and target_obj in objects)
    ]

    bindings_to_del = set()
    for key, binding_list in bindings.items():
        binding_list_copy = binding_list
        binding_list[:] = [
            (source_obj, target_obj, target_name, transform)
            for source_obj, target_obj, target_name, transform in binding_list_copy
            if not (isinstance(source_obj, type_) and source_obj in objects or
                    isinstance(target_obj, type_) and target_obj in objects)
        ]
        if not binding_list:
            bindings_to_del.add(key)
    for key in bindings_to_del:
        del bindings[key]

    for obj in objects:
        for name in bindable_properties_names.pop(id(obj)):
            bindable_properties.pop((id(obj), name), None)


def reset() -> None:
    """Clear all bindings.

    This function is intended for testing purposes only.
    """
    bindings.clear()
    bindable_properties.clear()
    bindable_properties_names.clear()
    active_links.clear()
