from nicegui import ui

from .examples import examples
from .style import example_link, link_target, section_heading


def create() -> None:
    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('examples')
        section_heading('In-depth examples', 'Pick your *solution*')
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4'):
            for example in examples:
                example_link(example)
