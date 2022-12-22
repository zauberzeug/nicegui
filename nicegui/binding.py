import asyncio
import logging
import time
from collections import defaultdict
from typing import Any, Callable, DefaultDict, Dict, List, Optional, Set, Tuple, Type

from . import globals

bindings: DefaultDict[Tuple[int, str], List] = defaultdict(list)
bindable_properties: Dict[Tuple[int, str], Any] = dict()
active_links: List[Tuple[Any, str, Any, str, Callable]] = []


async def loop():
    while True:
        visited: Set[Tuple[int, str]] = set()
        t = time.time()
        for link in active_links:
            (source_obj, source_name, target_obj, target_name, transform) = link
            value = transform(getattr(source_obj, source_name))
            if getattr(target_obj, target_name) != value:
                setattr(target_obj, target_name, value)
                propagate(target_obj, target_name, visited)
        if time.time() - t > 0.01:
            logging.warning(f'binding propagation for {len(active_links)} active links took {time.time() - t:.3f} s')
        await asyncio.sleep(globals.binding_refresh_interval)


def propagate(source_obj: Any, source_name: str, visited: Optional[Set[Tuple[int, str]]] = None) -> None:
    if visited is None:
        visited = set()
    visited.add((id(source_obj), source_name))
    for _, target_obj, target_name, transform in bindings.get((id(source_obj), source_name), []):
        if (id(target_obj), target_name) in visited:
            continue
        target_value = transform(getattr(source_obj, source_name))
        if getattr(target_obj, target_name) != target_value:
            setattr(target_obj, target_name, target_value)
            propagate(target_obj, target_name, visited)


def bind_to(self_obj: Any, self_name: str, other_obj: Any, other_name: str, forward: Callable) -> None:
    bindings[(id(self_obj), self_name)].append((self_obj, other_obj, other_name, forward))
    if (id(self_obj), self_name) not in bindable_properties:
        active_links.append((self_obj, self_name, other_obj, other_name, forward))
    propagate(self_obj, self_name)


def bind_from(self_obj: Any, self_name: str, other_obj: Any, other_name: str, backward: Callable) -> None:
    bindings[(id(other_obj), other_name)].append((other_obj, self_obj, self_name, backward))
    if (id(other_obj), other_name) not in bindable_properties:
        active_links.append((other_obj, other_name, self_obj, self_name, backward))
    propagate(other_obj, other_name)


def bind(self_obj: Any, self_name: str, other_obj: Any, other_name: str, *,
         forward: Callable = lambda x: x, backward: Callable = lambda x: x) -> None:
    bind_from(self_obj, self_name, other_obj, other_name, backward=backward)
    bind_to(self_obj, self_name, other_obj, other_name, forward=forward)


class BindableProperty:

    def __init__(self, on_change: Optional[Callable] = None) -> None:
        self.on_change = on_change

    def __set_name__(self, _, name: str) -> None:
        self.name = name

    def __get__(self, owner: Any, _=None) -> Any:
        return getattr(owner, '___' + self.name)

    def __set__(self, owner: Any, value: Any) -> None:
        has_attribute = hasattr(owner, '___' + self.name)
        value_changed = has_attribute and getattr(owner, '___' + self.name) != value
        if has_attribute and not value_changed:
            return
        setattr(owner, '___' + self.name, value)
        bindable_properties[(id(owner), self.name)] = owner
        propagate(owner, self.name)
        if value_changed and self.on_change is not None:
            self.on_change(owner, value)


def remove(objects: List[Any], type: Type) -> None:
    active_links[:] = [
        (source_obj, source_name, target_obj, target_name, transform)
        for source_obj, source_name, target_obj, target_name, transform in active_links
        if not (isinstance(source_obj, type) and source_obj in objects or
                isinstance(target_obj, type) and target_obj in objects)
    ]
    for key, binding_list in list(bindings.items()):
        binding_list[:] = [
            (source_obj, target_obj, target_name, transform)
            for source_obj, target_obj, target_name, transform in binding_list
            if not (isinstance(source_obj, type) and source_obj in objects or
                    isinstance(target_obj, type) and target_obj in objects)
        ]
        if not binding_list:
            del bindings[key]
    for (obj_id, name), obj in list(bindable_properties.items()):
        if isinstance(obj, type) and obj in objects:
            del bindable_properties[(obj_id, name)]
