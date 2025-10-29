from __future__ import annotations

import inspect
import sys
import types
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Generator, overload
from contextlib import contextmanager

import nicegui
from nicegui import app as nicegui_app
from nicegui import Client
from nicegui import ui as nicegui_ui
from nicegui.functions.navigate import Navigate
from nicegui.elements.markdown import remove_indentation

from .page import DocumentationPage
from .part import Demo, DocumentationPart

registry: dict[str, DocumentationPage] = {}
redirects: dict[str, str] = {}


@contextmanager
def dummy_client() -> Generator[Client, None, None]:
    """Create a dummy client for pre-rendering UI."""
    try:
        with Client(nicegui_ui.page('')) as client:
            yield client
    finally:
        client.delete()


def auto_execute(function: Callable) -> Callable:
    """Decorator to automatically execute the function when the module is imported."""
    with dummy_client():
        function()
    return function


def get_page(documentation: ModuleType) -> DocumentationPage:
    """Return the documentation page for the given documentation module."""
    target_name = documentation.__name__.split('.')[-1].removesuffix('_documentation')
    assert target_name in registry, f'Documentation page {target_name} does not exist'
    return registry[target_name]


def _get_current_page() -> DocumentationPage:
    frame = sys._getframe(2)  # pylint: disable=protected-access
    module = inspect.getmodule(frame)
    assert module is not None and module.__file__ is not None
    name = Path(module.__file__).stem.removesuffix('_documentation')
    if name == 'overview':
        name = ''
    if name not in registry:
        registry[name] = DocumentationPage(name=name)
    return registry[name]


def title(title_: str | None = None, subtitle: str | None = None) -> None:
    """Set the title of the current documentation page."""
    page = _get_current_page()
    page.title = title_
    page.subtitle = subtitle


def text(title_: str, description: str) -> None:
    """Add a text block to the current documentation page."""
    _get_current_page().parts.append(DocumentationPart(title=title_, description=description))


@overload
def demo(title_: str,
         description: str, /, *,
         tab: str | Callable | None = None,
         lazy: bool = True,
         ) -> Callable[[Callable], Callable]:
    ...


@overload
def demo(element: type, /,
         tab: str | Callable | None = None,
         lazy: bool = True,
         ) -> Callable[[Callable], Callable]:
    ...


@overload
def demo(function: Callable | Navigate, /,
         tab: str | Callable | None = None,
         lazy: bool = True,
         ) -> Callable[[Callable], Callable]:
    ...


def demo(*args, **kwargs) -> Callable[[Callable], Callable]:
    """Add a demo section to the current documentation page."""
    if len(args) == 2:
        element = None
        title_, description = args
        is_markdown = True
    else:
        element = args[0]
        doc = element.__doc__
        if isinstance(element, type) and not doc:
            doc = element.__init__.__doc__  # type: ignore
        title_, description = doc.split('\n', 1)
        title_ = title_.rstrip('.')
        is_markdown = False

    description = remove_indentation(description)
    page = _get_current_page()

    def decorator(function: Callable) -> Callable:
        if not page.parts and element:
            name = getattr(element, '__name__', None) or element.__class__.__name__
            ui_name = _find_attribute(nicegui_ui, name)
            app_name = _find_attribute(nicegui_app, name)
            if ui_name:
                page.title = f'ui.*{ui_name}*'
            elif app_name:
                page.title = f'app.*{app_name}*'
        page.parts.append(DocumentationPart(
            title=title_,
            description=description,
            description_format='md' if is_markdown else 'rst',
            demo=Demo(function=function, lazy=kwargs.get('lazy', True), tab=kwargs.get('tab')),
        ))
        return function
    return decorator


def part(title_: str) -> Callable:
    """Add a custom part with arbitrary UI and descriptive markdown elements to the current documentation page.

    The content of any contained markdown elements will be used for search indexing.
    """
    page = _get_current_page()

    def decorator(function: Callable) -> Callable:
        with dummy_client():
            with nicegui_ui.element():
                function()
                elements = nicegui.ElementFilter(kind=nicegui.ui.markdown, local_scope=True)
                description = ''.join(e.content for e in elements if '```' not in e.content)
        page.parts.append(DocumentationPart(title=title_, search_text=description, ui=function))
        return function
    return decorator


def ui(function: Callable) -> Callable:
    """Add arbitrary UI to the current documentation page."""
    _get_current_page().parts.append(DocumentationPart(ui=function))
    return function


def intro(documentation: types.ModuleType) -> None:
    """Add an intro section to the current documentation page."""
    current_page = _get_current_page()
    target_page = get_page(documentation)
    target_page.back_link = current_page.name
    part = deepcopy(target_page.parts[0])
    part.link = target_page.name
    current_page.parts.append(part)


def reference(element: type, *,
              title: str = 'Reference',  # pylint: disable=redefined-outer-name
              ) -> None:
    """Add a reference section to the current documentation page."""
    _get_current_page().parts.append(DocumentationPart(title=title, reference=element))


def extra_column(function: Callable) -> Callable:
    """Add an extra column to the current documentation page."""
    _get_current_page().extra_column = function
    return function


def _find_attribute(obj: Any, name: str) -> str | None:
    for attr in dir(obj):
        if attr.lower().replace('_', '') == name.lower().replace('_', ''):
            return attr
    return None
