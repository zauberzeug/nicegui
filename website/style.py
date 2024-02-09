import re
from typing import List, Optional

from nicegui import context, ui

from .examples import Example

SPECIAL_CHARACTERS = re.compile('[^(a-z)(A-Z)(0-9)-]')


def link_target(name: str, offset: str = '0') -> ui.link_target:
    """Create a link target that can be linked to with a hash."""
    target = ui.link_target(name).style(f'position: absolute; top: {offset}; left: 0')
    assert target.parent_slot is not None
    target.parent_slot.parent.classes('relative')
    return target


def section_heading(subtitle_: str, title_: str) -> None:
    """Render a section heading with a subtitle."""
    ui.label(subtitle_).classes('md:text-lg font-bold')
    ui.markdown(title_).classes('text-3xl md:text-5xl font-medium mt-[-12px] fancy-em')


def heading(title_: str) -> ui.markdown:
    """Render a heading."""
    return ui.markdown(title_).classes('text-2xl md:text-3xl xl:text-4xl font-medium text-white')


def title(content: str) -> ui.markdown:
    """Render a title."""
    return ui.markdown(content).classes('text-4xl sm:text-5xl md:text-6xl font-medium fancy-em')


def subtitle(content: str) -> ui.markdown:
    """Render a subtitle."""
    return ui.markdown(content).classes('text-xl sm:text-2xl md:text-3xl leading-7')


def example_link(example: Example) -> None:
    """Render a link to an example."""
    with ui.link(target=example.url) \
            .classes('bg-[#5898d420] p-4 self-stretch rounded flex flex-col gap-2') \
            .style('box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1)'):
        ui.label(example.title).classes(replace='font-bold')
        ui.markdown(example.description).classes(replace='bold-links arrow-links')


def features(icon: str, title_: str, items: List[str]) -> None:
    """Render a list of features."""
    with ui.column().classes('gap-1'):
        ui.icon(icon).classes('max-sm:hidden text-3xl md:text-5xl mb-3 text-primary opacity-80')
        ui.label(title_).classes('font-bold mb-3')
        ui.markdown('\n'.join(f'- {item}' for item in items)).classes('bold-links arrow-links -ml-4')


def side_menu() -> ui.left_drawer:
    """Render the side menu."""
    return ui.left_drawer() \
        .classes('column no-wrap gap-1 bg-[#eee] dark:bg-[#1b1b1b] mt-[-20px] px-8 py-20') \
        .style('height: calc(100% + 20px) !important')


def subheading(text: str, *, link: Optional[str] = None, major: bool = False, anchor_name: Optional[str] = None) -> None:
    """Render a subheading with an anchor that can be linked to with a hash."""
    name = anchor_name or create_anchor_name(text)
    ui.html(f'<div id="{name}"></div>').style('position: relative; top: -90px')
    with ui.row().classes('gap-2 items-center relative'):
        classes = 'text-3xl' if major else 'text-2xl'
        if link:
            ui.link(text, link).classes(classes)
        else:
            ui.label(text).classes(classes)
        with ui.link(target=f'#{name}').classes('absolute').style('transform: translateX(-150%)'):
            ui.icon('link', size='sm').classes('opacity-10 hover:opacity-80')
    drawers = [element for element in context.get_client().elements.values() if isinstance(element, ui.left_drawer)]
    if drawers:
        menu = drawers[0]
        with menu:
            async def click():
                if await ui.run_javascript('!!document.querySelector("div.q-drawer__backdrop")', timeout=5.0):
                    menu.hide()
                    ui.open(f'#{name}')
            ui.link(text, target=f'#{name}').props('data-close-overlay').on('click', click, []) \
                .classes('font-bold mt-4' if major else '')


def create_anchor_name(text: str) -> str:
    """Create an anchor name that can be linked to with a hash."""
    return SPECIAL_CHARACTERS.sub('_', text).lower()
