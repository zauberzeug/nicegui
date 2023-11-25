import re
from pathlib import Path
from typing import List, Optional

from nicegui import context, ui

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
    ui.markdown(title_).classes('text-3xl md:text-5xl font-medium mt-[-12px]')


def heading(title_: str) -> ui.markdown:
    """Render a heading."""
    return ui.markdown(title_).classes('text-2xl md:text-3xl xl:text-4xl font-medium text-white')


def title(content: str) -> ui.markdown:
    """Render a title."""
    return ui.markdown(content).classes('text-4xl sm:text-5xl md:text-6xl font-medium')


def subtitle(content: str) -> ui.markdown:
    """Render a subtitle."""
    return ui.markdown(content).classes('text-xl sm:text-2xl md:text-3xl leading-7')


def example_link(title_: str, description: str) -> None:
    """Render a link to an example."""
    name = title_.lower().replace(' ', '_')
    directory = Path(__file__).parent.parent / 'examples' / name
    content = [p for p in directory.glob('*') if p.name != '__pycache__' and not p.name.startswith('.')]
    filename = 'main.py' if len(content) == 1 else ''
    with ui.link(target=f'https://github.com/zauberzeug/nicegui/tree/main/examples/{name}/{filename}') \
            .classes('bg-[#5898d420] p-4 self-stretch rounded flex flex-col gap-2') \
            .style('box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1)'):
        ui.label(title_).classes(replace='font-bold')
        ui.markdown(description).classes(replace='bold-links arrow-links')


def features(icon: str, title_: str, items: List[str]) -> None:
    """Render a list of features."""
    with ui.column().classes('gap-1'):
        ui.icon(icon).classes('max-sm:hidden text-3xl md:text-5xl mb-3 text-primary opacity-80')
        ui.label(title_).classes('font-bold mb-3')
        for item in items:
            ui.markdown(f'- {item}').classes('bold-links arrow-links')


def side_menu() -> ui.left_drawer:
    """Render the side menu."""
    return ui.left_drawer() \
        .classes('column no-wrap gap-1 bg-[#eee] dark:bg-[#1b1b1b] mt-[-20px] px-8 py-20') \
        .style('height: calc(100% + 20px) !important')


def subheading(text: str, *, make_menu_entry: bool = True, link: Optional[str] = None) -> None:
    """Render a subheading with an anchor that can be linked to with a hash."""
    name = _create_anchor_name(text)
    ui.html(f'<div id="{name}"></div>').style('position: relative; top: -90px')
    with ui.row().classes('gap-2 items-center relative'):
        if link:
            ui.link(text, link).classes('text-2xl')
        else:
            ui.label(text).classes('text-2xl')
        with ui.link(target=f'#{name}').classes('absolute').style('transform: translateX(-150%)'):
            ui.icon('link', size='sm').classes('opacity-10 hover:opacity-80')
    if make_menu_entry:
        with _get_menu() as menu:
            async def click():
                if await ui.run_javascript('!!document.querySelector("div.q-drawer__backdrop")', timeout=5.0):
                    menu.hide()
                    ui.open(f'#{name}')
            ui.link(text, target=f'#{name}').props('data-close-overlay').on('click', click, [])


def _create_anchor_name(text: str) -> str:
    return SPECIAL_CHARACTERS.sub('_', text).lower()


def _get_menu() -> ui.left_drawer:
    return [element for element in context.get_client().elements.values() if isinstance(element, ui.left_drawer)][0]
