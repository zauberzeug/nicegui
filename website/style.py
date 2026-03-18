import re

from nicegui import ui

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


def example_link(example: Example | None = None) -> ui.link:
    """Render a link to an example."""
    with ui.link(target=example.url if example else '/examples') \
            .classes('bg-[#5898d420] p-4 self-stretch rounded flex flex-col gap-2') \
            .style('box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1)') as link:
        ui.label(example.title if example else '...and many more').classes(replace='font-bold')
        ui.markdown(example.description if example else 'Browse through plenty of examples.') \
            .classes(replace='bold-links arrow-links')
        if example:
            ui.space()
            ui.interactive_image(example.screenshot) \
                .classes('w-full object-contain border border-gray-300 rounded-md overflow-hidden aspect-16/9')
    return link


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
