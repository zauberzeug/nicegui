import importlib
import re
from typing import Callable, Optional, Union

import docutils.core

from nicegui import globals, ui
from nicegui.elements.markdown import apply_tailwind

from .example import example

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


def get_menu() -> ui.left_drawer:
    return [element for element in globals.get_client().elements.values() if isinstance(element, ui.left_drawer)][0]


def heading(text: str, *, make_menu_entry: bool = True) -> None:
    ui.html(f'<em>{text}</em>').classes('mt-8 text-3xl font-weight-500')
    if make_menu_entry:
        with get_menu():
            ui.label(text).classes('font-bold mt-4')


def subheading(text: str, *, make_menu_entry: bool = True) -> None:
    name = SPECIAL_CHARACTERS.sub('_', text).lower()
    target = ui.link_target(name).style('position: relative; top: -90px')
    with ui.row().classes('gap-2 items-center'):
        ui.label(text).classes('text-2xl')
        with ui.link(target=f'#{target.id}'):
            ui.icon('link', size='sm').classes('text-gray-400 hover:text-gray-800')
    if make_menu_entry:
        with get_menu() as menu:
            async def click():
                if await ui.run_javascript(f'!!document.querySelector("div.q-drawer__backdrop")'):
                    menu.hide()
                    ui.open(f'#{target.id}')
            ui.link(text, target=f'#{target.id}').props('data-close-overlay').on('click', click)


def markdown(text: str) -> None:
    ui.markdown(remove_indentation(text))


class text_example:

    def __init__(self, title: str, explanation: str) -> None:
        self.title = title
        self.explanation = explanation
        self.make_menu_entry = True

    def __call__(self, f: Callable) -> Callable:
        subheading(self.title, make_menu_entry=self.make_menu_entry)
        markdown(self.explanation)
        return example(None, None)(f)


class intro_example(text_example):

    def __init__(self, title: str, explanation: str) -> None:
        super().__init__(title, explanation)
        self.make_menu_entry = False


class element_example:

    def __init__(self, element_class: Union[Callable, type], browser_title: Optional[str] = None) -> None:
        self.element_class = element_class
        self.browser_title = browser_title

    def __call__(self, f: Callable) -> Callable:
        doc = self.element_class.__doc__ or self.element_class.__init__.__doc__
        title, documentation = doc.split('\n', 1)
        documentation = remove_indentation(documentation)
        documentation = documentation.replace('param ', '')
        html = docutils.core.publish_parts(documentation, writer_name='html5_polyglot')['html_body']
        html = apply_tailwind(html)
        with ui.column().classes('w-full mb-8 gap-2'):
            subheading(title)
            ui.html(html).classes('documentation bold-links arrow-links')
            return example(None, None, browser_title=self.browser_title)(f)


def load_example(element_class: type) -> None:
    def pascal_to_snake(name: str) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    name = pascal_to_snake(element_class.__name__)
    module = importlib.import_module(f'website.more_reference.{name}_reference')
    getattr(module, 'intro')()
