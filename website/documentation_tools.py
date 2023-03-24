import importlib
import inspect
import re
from typing import Callable, Optional, Union

import docutils.core

from nicegui import globals, ui
from nicegui.binding import BindableProperty
from nicegui.elements.markdown import apply_tailwind

from .demo import demo

SPECIAL_CHARACTERS = re.compile('[^(a-z)(A-Z)(0-9)-]')


def remove_indentation(text: str) -> str:
    """Remove indentation from a multi-line string based on the indentation of the first line."""
    lines = text.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        return ''
    indentation = len(lines[0]) - len(lines[0].lstrip())
    return '\n'.join(line[indentation:] for line in lines)


def pascal_to_snake(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def create_anchor_name(text: str) -> str:
    return SPECIAL_CHARACTERS.sub('_', text).lower()


def get_menu() -> ui.left_drawer:
    return [element for element in globals.get_client().elements.values() if isinstance(element, ui.left_drawer)][0]


def heading(text: str, *, make_menu_entry: bool = True) -> None:
    ui.html(f'<em>{text}</em>').classes('mt-8 text-3xl font-weight-500')
    if make_menu_entry:
        with get_menu():
            ui.label(text).classes('font-bold mt-4')


def subheading(text: str, *, make_menu_entry: bool = True) -> None:
    name = create_anchor_name(text)
    ui.html(f'<div id="{name}"></div>').style('position: relative; top: -90px')
    with ui.row().classes('gap-2 items-center'):
        ui.label(text).classes('text-2xl')
        with ui.link(target=f'#{name}'):
            ui.icon('link', size='sm').classes('text-gray-400 hover:text-gray-800')
    if make_menu_entry:
        with get_menu() as menu:
            async def click():
                if await ui.run_javascript(f'!!document.querySelector("div.q-drawer__backdrop")'):
                    menu.hide()
                    ui.open(f'#{name}')
            ui.link(text, target=f'#{name}').props('data-close-overlay').on('click', click)


def markdown(text: str) -> ui.markdown:
    return ui.markdown(remove_indentation(text))


def render_docstring(doc: str) -> ui.html:
    doc = remove_indentation(doc)
    doc = doc.replace('param ', '')
    html = docutils.core.publish_parts(doc, writer_name='html5_polyglot')['html_body']
    html = apply_tailwind(html)
    return ui.html(html).classes('documentation bold-links arrow-links')


class text_demo:

    def __init__(self, title: str, explanation: str) -> None:
        self.title = title
        self.explanation = explanation
        self.make_menu_entry = True

    def __call__(self, f: Callable) -> Callable:
        subheading(self.title, make_menu_entry=self.make_menu_entry)
        markdown(self.explanation)
        return demo()(f)


class intro_demo(text_demo):

    def __init__(self, title: str, explanation: str) -> None:
        super().__init__(title, explanation)
        self.make_menu_entry = False


class element_demo:

    def __init__(self, element_class: Union[Callable, type], browser_title: Optional[str] = None) -> None:
        self.element_class = element_class
        self.browser_title = browser_title

    def __call__(self, f: Callable, *, more_link: Optional[str] = None) -> Callable:
        doc = self.element_class.__doc__ or self.element_class.__init__.__doc__
        title, documentation = doc.split('\n', 1)
        with ui.column().classes('w-full mb-8 gap-2'):
            subheading(title)
            render_docstring(documentation)
            wrapped = demo(browser_title=self.browser_title)(f)
            if more_link:
                ui.markdown(f'[More...](documentation/{more_link})').classes('bold-links mt-2')
            return wrapped


def load_demo(element_class: type) -> None:
    name = pascal_to_snake(element_class.__name__)
    try:
        module = importlib.import_module(f'website.more_documentation.{name}_documentation')
    except ModuleNotFoundError:
        module = importlib.import_module(f'website.more_documentation.{name.replace("_", "")}_documentation')
    element_demo(element_class)(getattr(module, 'main_demo'), more_link=name)


def is_method_or_property(cls: type, attribute_name: str) -> bool:
    attribute = cls.__dict__.get(attribute_name, None)
    return (
        inspect.isfunction(attribute) or
        inspect.ismethod(attribute) or
        isinstance(attribute, property) or
        isinstance(attribute, BindableProperty)
    )


def generate_class_doc(class_obj: type) -> None:
    mro = [base for base in class_obj.__mro__ if base.__module__.startswith('nicegui.')]
    ancestors = mro[1:]
    attributes = {}
    for base in reversed(mro):
        for name in dir(base):
            if not name.startswith('_') and is_method_or_property(base, name):
                attributes[name] = getattr(base, name, None)
    properties = {name: attribute for name, attribute in attributes.items() if not callable(attribute)}
    methods = {name: attribute for name, attribute in attributes.items() if callable(attribute)}

    if properties:
        subheading('Properties')
        with ui.column().classes('gap-2'):
            for name, property in sorted(properties.items()):
                ui.markdown(f'**`{name}`**`{generate_property_signature_description(property)}`')
                if property.__doc__:
                    render_docstring(property.__doc__).classes('ml-8')
    if methods:
        subheading('Methods')
        with ui.column().classes('gap-2'):
            for name, method in sorted(methods.items()):
                ui.markdown(f'**`{name}`**`{generate_method_signature_description(method)}`')
                if method.__doc__:
                    render_docstring(method.__doc__).classes('ml-8')
    if ancestors:
        subheading('Inherited from')
        with ui.column().classes('gap-2'):
            for ancestor in ancestors:
                ui.markdown(f'- `{ancestor.__name__}`')


def generate_method_signature_description(method: Callable) -> str:
    param_strings = []
    for param in inspect.signature(method).parameters.values():
        param_string = param.name
        if param_string == 'self':
            continue
        if param.annotation != inspect.Parameter.empty:
            param_type = inspect.formatannotation(param.annotation)
            param_string += f''': {param_type.strip("'")}'''
        if param.default != inspect.Parameter.empty:
            param_string += f' = [...]' if callable(param.default) else f' = {repr(param.default)}'
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_string = f'*{param_string}'
        param_strings.append(param_string)
    method_signature = ', '.join(param_strings)
    description = f'({method_signature})'
    return_annotation = inspect.signature(method).return_annotation
    if return_annotation != inspect.Parameter.empty:
        return_type = inspect.formatannotation(return_annotation)
        description += f''' -> {return_type.strip("'").replace("typing_extensions.", "").replace("typing.", "")}'''
    return description


def generate_property_signature_description(property: Optional[property]) -> str:
    description = ''
    if property is None:
        return ': BindableProperty'
    if property.fget:
        return_annotation = inspect.signature(property.fget).return_annotation
        if return_annotation != inspect.Parameter.empty:
            return_type = inspect.formatannotation(return_annotation)
            description += f': {return_type}'
    if property.fset:
        description += ' (settable)'
    if property.fdel:
        description += ' (deletable)'
    return description
