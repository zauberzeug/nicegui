import asyncio
import logging
import time
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Callable, Optional, Set, Tuple

from justpy.htmlcomponents import HTMLBaseComponent

from . import globals
from .task_logger import create_task

bindings = defaultdict(list)
bindable_properties = dict()
active_links = []


async def loop():
    while True:
        visited: Set[Tuple[int, str]] = set()
        visited_views: Set[HTMLBaseComponent] = set()
        t = time.time()
        for link in active_links:
            (source_obj, source_name, target_obj, target_name, transform) = link
            value = transform(getattr(source_obj, source_name))
            if getattr(target_obj, target_name) != value:
                setattr(target_obj, target_name, value)
                propagate(target_obj, target_name, visited, visited_views)
        if time.time() - t > 0.01:
            logging.warning(f'binding propagation for {len(active_links)} active links took {time.time() - t:.3f} s')
        t = time.time()
        update_views(visited_views)
        if time.time() - t > 0.01:
            logging.warning(f'binding update for {len(visited_views)} visited views took {time.time() - t:.3f} s')
        await asyncio.sleep(globals.config.binding_refresh_interval)


async def update_views_async(views: Set[HTMLBaseComponent]):
    for view in views:
        await view.update()


def update_views(views: Set[HTMLBaseComponent]):
    if globals.loop is None:
        return  # NOTE: no need to update view if event loop is not running, yet
    create_task(update_views_async(views), name='update_views_async')


def propagate(source_obj: Any,
              source_name: str,
              visited: Set[Tuple[int, str]] = None,
              visited_views: Set[HTMLBaseComponent] = None) -> Set[HTMLBaseComponent]:
    if visited is None:
        visited = set()
    if visited_views is None:
        visited_views = set()
    visited.add((id(source_obj), source_name))
    if isinstance(source_obj, HTMLBaseComponent):
        visited_views.add(source_obj)
    for _, target_obj, target_name, transform in bindings[(id(source_obj), source_name)]:
        if (id(target_obj), target_name) in visited:
            continue
        target_value = transform(getattr(source_obj, source_name))
        if getattr(target_obj, target_name) != target_value:
            setattr(target_obj, target_name, target_value)
            propagate(target_obj, target_name, visited, visited_views)
    return visited_views


def bind_to(self_obj: Any, self_name: str, other_obj: Any, other_name: str, forward: Callable) -> None:
    bindings[(id(self_obj), self_name)].append((self_obj, other_obj, other_name, forward))
    if (id(self_obj), self_name) not in bindable_properties:
        active_links.append((self_obj, self_name, other_obj, other_name, forward))
    update_views(propagate(self_obj, self_name))


def bind_from(self_obj: Any, self_name: str, other_obj: Any, other_name: str, backward: Callable) -> None:
    bindings[(id(other_obj), other_name)].append((other_obj, self_obj, self_name, backward))
    if (id(other_obj), other_name) not in bindable_properties:
        active_links.append((other_obj, other_name, self_obj, self_name, backward))
    update_views(propagate(other_obj, other_name))


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
        update_views(propagate(owner, self.name))
        if value_changed and self.on_change is not None:
            self.on_change(owner, value)


class BindTextMixin(ABC):
    """
    Mixin providing bind methods for attribute text.
    """
    text = BindableProperty()

    def bind_text_to(self, target_object: Any, target_name: str, forward: Callable = lambda x: x):
        bind_to(self, 'text', target_object, target_name, forward)
        return self

    def bind_text_from(self, target_object: Any, target_name: str, backward: Callable = lambda x: x):
        bind_from(self, 'text', target_object, target_name, backward)
        return self

    def bind_text(self, target_object: Any, target_name: str, *,
                  forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        bind(self, 'text', target_object, target_name, forward=forward, backward=backward)
        return self

    @property
    @abstractmethod
    def text(self) -> str:
        pass

    @text.setter
    @abstractmethod
    def text(self, text: str) -> None:
        pass

    def set_text(self, text: str) -> None:
        self.text = text


class BindValueMixin:
    """
    Mixin providing bind methods for attribute value.
    """

    def bind_value_to(self, target_object: Any, target_name: str, forward: Callable = lambda x: x):
        bind_to(self, 'value', target_object, target_name, forward)
        return self

    def bind_value_from(self, target_object: Any, target_name: str, backward: Callable = lambda x: x):
        bind_from(self, 'value', target_object, target_name, backward)
        return self

    def bind_value(self, target_object: Any, target_name: str, *,
                   forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        bind(self, 'value', target_object, target_name, forward=forward, backward=backward)
        return self


class BindContentMixin:
    """
    Mixin providing bind methods for attribute content.
    """

    def bind_content_to(self, target_object: Any, target_name: str, forward: Callable = lambda x: x):
        bind_to(self, 'content', target_object, target_name, forward)
        return self

    def bind_content_from(self, target_object: Any, target_name: str, backward: Callable = lambda x: x):
        bind_from(self, 'content', target_object, target_name, backward)
        return self

    def bind_content(self, target_object: Any, target_name: str, *,
                     forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        bind(self, 'content', target_object, target_name, forward=forward, backward=backward)
        return self


class BindVisibilityMixin:
    """
    Mixin providing bind methods for attribute visible.
    """

    def bind_visibility_to(self, target_object: Any, target_name: str, forward: Callable = lambda x: x):
        bind_to(self, 'visible', target_object, target_name, forward)
        return self

    def bind_visibility_from(self, target_object: Any, target_name: str, backward: Callable = lambda x: x, *,
                             value: Any = None):
        if value is not None:
            def backward(x): return x == value
        bind_from(self, 'visible', target_object, target_name, backward)
        return self

    def bind_visibility(self, target_object: Any, target_name: str,  *,
                        forward: Callable = lambda x: x, backward: Callable = lambda x: x, value: Any = None):
        if value is not None:
            def backward(x): return x == value
        bind(self, 'visible', target_object, target_name, forward=forward, backward=backward)
        return self


class BindSourceMixin:
    """
    Mixin providing bind methods for attribute source.
    """

    def bind_source_to(self, target_object: Any, target_name: str, forward: Callable = lambda x: x):
        bind_to(self, 'source', target_object, target_name, forward)
        return self

    def bind_source_from(self, target_object: Any, target_name: str, backward: Callable = lambda x: x):
        bind_from(self, 'source', target_object, target_name, backward)
        return self

    def bind_source(self, target_object: Any, target_name: str, *,
                    forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        bind(self, 'source', target_object, target_name, forward=forward, backward=backward)
        return self
