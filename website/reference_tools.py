import re
from typing import Callable

from nicegui import globals, ui

from .example import example

SPECIAL_CHARACTERS = re.compile('[^(a-z)(A-Z)(0-9)-]')


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
        with get_menu():
            ui.link(text, target=f'#{target.id}').classes('block py-1 px-2 hover:bg-gray-100')


class intro_example:

    def __init__(self, title: str, explanation: str) -> None:
        self.title = title
        self.explanation = explanation

    def __call__(self, f: Callable) -> Callable:
        subheading(self.title, make_menu_entry=False)
        ui.label(self.explanation)
        return example(None, None)(f)
