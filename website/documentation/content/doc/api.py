from __future__ import annotations

import inspect
import sys
import types
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Dict, Optional, Union, overload

from nicegui import app as nicegui_app
from nicegui import ui as nicegui_ui
from nicegui.elements.markdown import remove_indentation

from .page import DocumentationPage
from .part import Demo, DocumentationPart

registry: Dict[str, DocumentationPage] = {}


def get_page(documentation: ModuleType) -> DocumentationPage:
    """
    Return the documentation page for the given documentation module.

    Parameters:
        documentation (ModuleType): The documentation module for which to retrieve the page.

    Returns:
        DocumentationPage: The documentation page corresponding to the given module.

    Raises:
        AssertionError: If the documentation page does not exist in the registry.

    This function retrieves the documentation page associated with the given documentation module.
    It first determines the target name by removing the suffix '_documentation' from the module's name.
    Then it checks if the target name exists in the registry dictionary.
    If the target name is found, the corresponding documentation page is returned.
    If the target name is not found, an AssertionError is raised.

    Example:
        # Assuming 'my_module_documentation' exists in the registry
        page = get_page(my_module_documentation)
    """
    target_name = _removesuffix(documentation.__name__.split('.')[-1], '_documentation')
    assert target_name in registry, f'Documentation page {target_name} does not exist'
    return registry[target_name]


def _get_current_page() -> DocumentationPage:
    """
    Retrieves the current documentation page based on the calling module.

    This function inspects the calling module and retrieves its name. If the name is 'overview', it is changed to an empty string.
    The function then checks if the name exists in the registry. If not, a new DocumentationPage object is created and added to the registry.
    Finally, the function returns the DocumentationPage object associated with the module name.

    Returns:
        DocumentationPage: The current documentation page.

    Raises:
        AssertionError: If the calling module or its file path is not available.

    """
    frame = sys._getframe(2)  # pylint: disable=protected-access
    module = inspect.getmodule(frame)
    assert module is not None and module.__file__ is not None
    name = _removesuffix(Path(module.__file__).stem, '_documentation')
    if name == 'overview':
        name = ''
    if name not in registry:
        registry[name] = DocumentationPage(name=name)
    return registry[name]


def title(title_: Optional[str] = None, subtitle: Optional[str] = None) -> None:
    """
    Set the title of the current documentation page.

    Args:
        title_ (Optional[str]): The main title of the page.
        subtitle (Optional[str]): The subtitle of the page.

    Returns:
        None
    """
    page = _get_current_page()
    page.title = title_
    page.subtitle = subtitle


def text(title_: str, description: str) -> None:
    """
    Add a text block to the current documentation page.

    Args:
        title_ (str): The title of the text block.
        description (str): The description of the text block.

    Returns:
        None

    Raises:
        None
    """
    _get_current_page().parts.append(DocumentationPart(title=title_, description=description, description_format='md'))


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
    """
    Add a demo section to the current documentation page.

    Args:
        *args: Variable length arguments. If two arguments are provided, they are treated as `title` and `description`.
               If more than two arguments are provided, the first argument is treated as `element` and the remaining
               arguments are ignored.
        **kwargs: Keyword arguments. The following keyword arguments are supported:
            - lazy (bool): If True, the demo will be loaded lazily. Defaults to True.
            - tab (str): The tab name to display the demo in. Defaults to None.

    Returns:
        Callable: A decorator function that can be used to add a demo section to a documentation page.

    Usage:
        @demo("Demo Title", "Demo Description")
        def my_demo_function():
            # Code for the demo

        @demo(MyElement, lazy=False, tab="My Tab")
        def my_element_demo():
            # Code for the demo

    """
    if len(args) == 2:
        element = None
        title_, description = args
        is_markdown = True
    else:
        element = args[0]
        doc = element.__init__.__doc__ if isinstance(element, type) else element.__doc__  # type: ignore
        title_, description = doc.split('\n', 1)
        is_markdown = False

    description = remove_indentation(description)
    page = _get_current_page()

    def decorator(function: Callable) -> Callable:
        if not page.parts and element:
            ui_name = _find_attribute(nicegui_ui, element.__name__)
            app_name = _find_attribute(nicegui_app, element.__name__)
            if ui_name:
                page.title = f'ui.*{ui_name}*'
            if app_name:
                page.title = f'app.*{app_name}*'
        page.parts.append(DocumentationPart(
            title=title_,
            description=description,
            description_format='md' if is_markdown else 'rst',
            demo=Demo(function=function, lazy=kwargs.get('lazy', True), tab=kwargs.get('tab')),
        ))
        return function
    return decorator


def ui(function: Callable) -> Callable:
    """
    Decorator to add arbitrary UI to the current documentation page.

    This decorator can be used to add custom UI elements to the current documentation page.
    It takes a function as input, which will be called to generate the UI content.
    The function should accept no arguments and return a string representing the UI content.

    Example usage:
    ```
    @ui
    def my_custom_ui():
        return "<h1>Hello, World!</h1>"
    ```

    The `my_custom_ui` function will be called when the documentation page is rendered,
    and the returned string will be added to the page.

    Returns:
        Callable: The decorated function.
    """
    _get_current_page().parts.append(DocumentationPart(ui=function))
    return function


def intro(documentation: types.ModuleType) -> None:
    """
    Add an intro section to the current documentation page.

    Args:
        documentation (types.ModuleType): The module containing the documentation.

    Returns:
        None

    Description:
        This function adds an introductory section to the current documentation page.
        It takes the `documentation` module as input and modifies the current page
        by adding a new section with a link to the target page.
    """
    current_page = _get_current_page()
    target_page = get_page(documentation)
    target_page.back_link = current_page.name
    part = deepcopy(target_page.parts[0])
    part.link = target_page.name
    current_page.parts.append(part)


def reference(element: type, *,
              title: str = 'Reference',  # pylint: disable=redefined-outer-name
              ) -> None:
    """
    Add a reference section to the current documentation page.

    Parameters:
        element (type): The element to be referenced.
        title (str, optional): The title of the reference section. Defaults to 'Reference'.

    Returns:
        None

    Raises:
        None

    Example:
        # Add a reference section for a class
        reference(MyClass, title='MyClass Reference')
    """
    _get_current_page().parts.append(DocumentationPart(title=title, reference=element))

def extra_column(function: Callable) -> Callable:
    """
    Add an extra column to the current documentation page.

    This decorator function is used to add an extra column to the current documentation page.
    It takes a function as an argument, which will be called to generate the content for the extra column.

    Parameters:
        function (Callable): The function that generates the content for the extra column.

    Returns:
        Callable: The decorated function.

    Example:
        @extra_column
        def my_extra_column():
            return "This is the content for the extra column."

        The above example adds an extra column to the current documentation page, and the content
        for the extra column is generated by the `my_extra_column` function.

    Note:
        The `extra_column` decorator should be used on functions that return a string or HTML content
        to be displayed in the extra column.

    """
    _get_current_page().extra_column = function
    return function


def _find_attribute(obj: Any, name: str) -> Optional[str]:
    """
    Find an attribute in an object by name, ignoring case and underscores.

    This function searches for an attribute in the given object by comparing its name
    (ignoring case and underscores) with the provided name. If a matching attribute is found,
    its name is returned. Otherwise, None is returned.

    Args:
        obj (Any): The object to search for the attribute in.
        name (str): The name of the attribute to find.

    Returns:
        Optional[str]: The name of the matching attribute, or None if no match is found.
    """
    for attr in dir(obj):
        if attr.lower().replace('_', '') == name.lower().replace('_', ''):
            return attr
    return None


def _removesuffix(string: str, suffix: str) -> str:
    """
    Remove a suffix from a string if it exists.

    Args:
        string (str): The input string.
        suffix (str): The suffix to be removed from the string.

    Returns:
        str: The modified string with the suffix removed.

    Notes:
        This function is intended to be used as a workaround for Python versions prior to 3.9,
        which do not have the built-in `str.removesuffix()` method.

    Example:
        >>> _removesuffix("hello world", "world")
        'hello '

    """
    if string.endswith(suffix):
        return string[:-len(suffix)]
    return string
