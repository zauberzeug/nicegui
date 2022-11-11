import asyncio
import logging
import time
from collections import defaultdict
from typing import Any, Callable, Optional, Set, Tuple

from justpy.htmlcomponents import HTMLBaseComponent

from . import globals
from .task_logger import create_task
from .updatable import Updatable

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


class BindableProperty:

    def __init__(self, on_change: Optional[Callable] = None) -> None:
        self.on_change = on_change

    def __set_name__(self, _, name: str) -> None:
        self.name = name

    def __get__(self, owner: Any, _=None) -> Any:
        return getattr(owner, '_' + self.name)

    def __set__(self, owner: Any, value: Any) -> None:
        has_attribute = hasattr(owner, '_' + self.name)
        value_changed = has_attribute and getattr(owner, '_' + self.name) != value
        if has_attribute and not value_changed:
            return
        setattr(owner, '_' + self.name, value)
        bindable_properties[(id(owner), self.name)] = owner
        update_views(propagate(owner, self.name))
        if value_changed and self.on_change is not None:
            self.on_change(owner, value)


class BindMixin(Updatable):
    """
    Mixin providing bind methods for target object attributes.
    """

    def _bind_from(self, target_object: Any, target_name: str, *, attr: str, backward=lambda x: x):
        bind_from(self, attr, target_object, target_name, backward=backward)
        return self

    def _bind_to(self, target_object: Any, target_name: str, *, attr: str, forward=lambda x: x):
        bind_to(self, attr, target_object, target_name, forward=forward)
        return self

    def _bind(self, target_object: Any, target_name: str, *, attr: str, forward=lambda x: x, backward=lambda x: x):
        self._bind_from(target_object, target_name, attr=attr, backward=backward)
        self._bind_to(target_object, target_name, attr=attr, forward=forward)
        return self


class BindTextMixin(BindMixin):
    """
    Mixin providing bind methods for attribute text.
    """
    text = BindableProperty()

    def bind_text_to(self, target_object: Any, target_name: str, forward: Callable = lambda x: x):
        return super()._bind_to(target_object, target_name, attr='text', forward=forward)

    def bind_text_from(self, target_object: Any, target_name: str, backward: Callable = lambda x: x):
        return super()._bind_from(target_object, target_name, attr='text', backward=backward)

    def bind_text(self, target_object: Any, target_name: str, forward: Callable = lambda x: x, backward=lambda x: x):
        self.bind_text_from(target_object, target_name, backward=backward)
        self.bind_text_to(target_object, target_name, forward=forward)
        return self

    @property
    def text(self) -> str:
        return self._content

    @text.setter
    def text(self, text: str) -> None:
        self.set_text(text)

    def set_text(self, text: str) -> None:
        self._content = text
        self.update()


class BindValueMixin(BindMixin):
    """
    Mixin providing bind methods for attribute value.
    """

    def bind_value_to(self, target_object: Any, target_name: str, forward: Callable = lambda x: x):
        return super()._bind_to(target_object, target_name, attr='value', forward=forward)

    def bind_value_from(self, target_object: Any, target_name: str, backward: Callable = lambda x: x):
        return super()._bind_from(target_object, target_name, attr='value', backward=backward)

    def bind_value(self, target_object, target_name, forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        self.bind_value_from(target_object, target_name, backward=backward)
        self.bind_value_to(target_object, target_name, forward=forward)
        return self


class BindContentMixin(BindMixin):
    """
    Mixin providing bind methods for attribute content.
    """

    def bind_content_to(self, target_object: Any, target_name: str, forward: Callable = lambda x: x):
        return super()._bind_to(target_object, target_name, attr='content', forward=forward)

    def bind_content_from(self, target_object: Any, target_name: str, backward: Callable = lambda x: x):
        return super()._bind_from(target_object, target_name, attr='content', backward=backward)

    def bind_content(self, target_object: Any, target_name: str,
                     forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        self.bind_content_from(target_object, target_name, backward=backward)
        self.bind_content_to(target_object, target_name, forward=forward)
        return self


class BindVisibilityMixin(BindMixin):
    """
    Mixin providing bind methods for attribute visible.
    """

    def bind_visibility_to(self, target_object: Any, target_name: str, forward: Callable = lambda x: x):
        return super()._bind_to(target_object, target_name, attr='visible', forward=forward)

    def bind_visibility_from(self, target_object: Any, target_name: str,
                             backward: Callable = lambda x: x, *, value: Any = None):
        if value is not None:
            def backward(x): return x == value
        return super()._bind_from(target_object, target_name, attr='visible', backward=backward)

    def bind_visibility(self, target_object: Any, target_name: str,
                        forward: Callable = lambda x: x, backward: Callable = lambda x: x, *, value: Any = None):
        if value is not None:
            def backward(x): return x == value
        self.bind_visibility_from(target_object, target_name, backward=backward)
        self.bind_visibility_to(target_object, target_name, forward=forward)
        return self


class BindSourceMixin(BindMixin):
    """
    Mixin providing bind methods for attribute source.
    """

    def bind_source_to(self, target_object: Any, target_name: str, forward: Callable = lambda x: x):
        return super()._bind_to(target_object, target_name, attr='source', forward=forward)

    def bind_source_from(self, target_object: Any, target_name: str, backward: Callable = lambda x: x):
        return super()._bind_from(target_object, target_name, attr='source', backward=backward)

    def bind_source(self, target_object: Any, target_name: str,
                    forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        self.bind_source_from(target_object, target_name, backward=backward)
        self.bind_source_to(target_object, target_name, forward=forward)
        return self
