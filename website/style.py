import re

from nicegui import ui

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


def subheading(text: str, *, link: str | None = None, major: bool = False, anchor_name: str | None = None) -> None:
    """Render a subheading with an anchor that can be linked to with a hash."""
    name = anchor_name or create_anchor_name(text)
    ui.html(f'<div id="{name}"></div>', sanitize=False).style('position: relative; top: -90px')
    with ui.row().classes('gap-2 items-center relative'):
        classes = 'text-3xl' if major else 'text-2xl'
        if link:
            ui.link(text, link).classes(classes)
        else:
            ui.label(text).classes(classes)
        with ui.link(target=f'#{name}').classes('absolute').style('transform: translateX(-150%)'):
            ui.icon('link', size='sm').classes('opacity-10 hover:opacity-80')


def create_anchor_name(text: str) -> str:
    """Create an anchor name that can be linked to with a hash."""
    return SPECIAL_CHARACTERS.sub('_', text).lower()
