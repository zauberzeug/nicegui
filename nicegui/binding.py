import asyncio
import logging
import time
from collections import defaultdict
from typing import Any, Callable, Optional, Set, Tuple

from . import globals

bindings = defaultdict(list)
bindable_properties = dict()
active_links = []


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


def propagate(source_obj: Any, source_name: str, visited: Set[Tuple[int, str]] = None) -> None:
    if visited is None:
        visited = set()
    visited.add((id(source_obj), source_name))
    for _, target_obj, target_name, transform in bindings[(id(source_obj), source_name)]:
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


class BindTextMixin:
    """
    Mixin providing bind methods for attribute text.
    """
    text = BindableProperty(on_change=lambda sender, text: sender.on_text_change(text))

    def bind_text_to(self, target_object: Any, target_name: str = 'text', forward: Callable = lambda x: x):
        bind_to(self, 'text', target_object, target_name, forward)
        return self

    def bind_text_from(self, target_object: Any, target_name: str = 'text', backward: Callable = lambda x: x):
        bind_from(self, 'text', target_object, target_name, backward)
        return self

    def bind_text(self, target_object: Any, target_name: str = 'text', *,
                  forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        bind(self, 'text', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_text(self, text: str) -> None:
        self.text = text

    def on_text_change(self, text: str) -> None:
        pass


class BindValueMixin:
    """
    Mixin providing bind methods for attribute value.
    """
    value = BindableProperty(on_change=lambda sender, value: sender.on_value_change(value))

    def bind_value_to(self, target_object: Any, target_name: str = 'value', forward: Callable = lambda x: x):
        bind_to(self, 'value', target_object, target_name, forward)
        return self

    def bind_value_from(self, target_object: Any, target_name: str = 'value', backward: Callable = lambda x: x):
        bind_from(self, 'value', target_object, target_name, backward)
        return self

    def bind_value(self, target_object: Any, target_name: str = 'value', *,
                   forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        bind(self, 'value', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_value(self, value: str) -> None:
        self.value = value

    def on_value_change(self, value: str) -> None:
        pass


class BindContentMixin:
    """
    Mixin providing bind methods for attribute content.
    """
    content = BindableProperty(on_change=lambda sender, content: sender.on_content_change(content))

    def bind_content_to(self, target_object: Any, target_name: str = 'content', forward: Callable = lambda x: x):
        bind_to(self, 'content', target_object, target_name, forward)
        return self

    def bind_content_from(self, target_object: Any, target_name: str = 'content', backward: Callable = lambda x: x):
        bind_from(self, 'content', target_object, target_name, backward)
        return self

    def bind_content(self, target_object: Any, target_name: str = 'content', *,
                     forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        bind(self, 'content', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_content(self, content: str) -> None:
        self.content = content

    def on_content_change(self, content: str) -> None:
        pass


class BindVisibilityMixin:
    """
    Mixin providing bind methods for attribute visible.
    """
    visibility = BindableProperty(on_change=lambda sender, visibility: sender.on_visibility_change(visibility))

    def bind_visibility_to(self, target_object: Any, target_name: str = 'visibility', forward: Callable = lambda x: x):
        bind_to(self, 'visible', target_object, target_name, forward)
        return self

    def bind_visibility_from(self, target_object: Any, target_name: str = 'visibility',
                             backward: Callable = lambda x: x, *, value: Any = None):
        if value is not None:
            def backward(x): return x == value
        bind_from(self, 'visible', target_object, target_name, backward)
        return self

    def bind_visibility(self, target_object: Any, target_name: str = 'visibility', *,
                        forward: Callable = lambda x: x, backward: Callable = lambda x: x, value: Any = None):
        if value is not None:
            def backward(x): return x == value
        bind(self, 'visible', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_visibility(self, visibility: str) -> None:
        self.visibility = visibility

    def on_visibility_change(self, visibility: str) -> None:
        pass


class BindSourceMixin:
    """
    Mixin providing bind methods for attribute source.
    """
    source = BindableProperty(on_change=lambda sender, source: sender.on_source_change(source))

    def bind_source_to(self, target_object: Any, target_name: str = 'source', forward: Callable = lambda x: x):
        bind_to(self, 'source', target_object, target_name, forward)
        return self

    def bind_source_from(self, target_object: Any, target_name: str = 'source', backward: Callable = lambda x: x):
        bind_from(self, 'source', target_object, target_name, backward)
        return self

    def bind_source(self, target_object: Any, target_name: str = 'source', *,
                    forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        bind(self, 'source', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_source(self, source: str) -> None:
        self.source = source

    def on_source_change(self, source: str) -> None:
        pass
