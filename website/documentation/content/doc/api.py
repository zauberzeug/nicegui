from __future__ import annotations

import inspect
import sys
import types
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from typing import Callable, Dict, Optional, Union, overload

from nicegui.elements.markdown import remove_indentation

from .page import DocumentationPage
from .part import Demo, DocumentationPart

registry: Dict[str, DocumentationPage] = {}


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
    if name not in registry:
        registry[name] = DocumentationPage(name=name)
    return registry[name]


def title(title_: Optional[str] = None, subtitle: Optional[str] = None) -> None:
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
         tab: Optional[Union[str, Callable]] = None,
         lazy: bool = True,
         ) -> Callable[[Callable], Callable]:
    ...


@overload
def demo(element: type, /,
         tab: Optional[Union[str, Callable]] = None,
         lazy: bool = True,
         ) -> Callable[[Callable], Callable]:
    ...


@overload
def demo(function: Callable, /,
         tab: Optional[Union[str, Callable]] = None,
         lazy: bool = True,
         ) -> Callable[[Callable], Callable]:
    ...


def demo(*args, **kwargs) -> Callable[[Callable], Callable]:
    """Add a demo section to the current documentation page."""
    if len(args) == 2:
        title_, description = args
        is_markdown = True
    else:
        doc = args[0].__init__.__doc__ if isinstance(args[0], type) else args[0].__doc__  # type: ignore
        title_, description = doc.split('\n', 1)
        is_markdown = False

    description = remove_indentation(description)
    page = _get_current_page()

    def decorator(function: Callable) -> Callable:
        page.parts.append(DocumentationPart(
            title=title_,
            description=description,
            description_format='md' if is_markdown else 'rst',
            demo=Demo(function=function, lazy=kwargs.get('lazy', True)),
        ))
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
