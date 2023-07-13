from pathlib import Path
from typing import List

from nicegui import ui


def link_target(name: str, offset: str = '0') -> ui.link_target:
    target = ui.link_target(name).style(f'position: absolute; top: {offset}; left: 0')
    target.parent_slot.parent.classes('relative')
    return target


def section_heading(subtitle: str, title: str) -> None:
    ui.label(subtitle).classes('md:text-lg font-bold')
    ui.markdown(title).classes('text-3xl md:text-5xl font-medium mt-[-12px]')


def heading(title: str) -> ui.label:
    return ui.markdown(title).classes('text-2xl md:text-3xl xl:text-4xl font-medium text-white')


def title(content: str) -> ui.markdown:
    return ui.markdown(content).classes('text-4xl sm:text-5xl md:text-6xl font-medium')


def subtitle(content: str) -> ui.markdown:
    return ui.markdown(content).classes('text-xl sm:text-2xl md:text-3xl leading-7')


def example_link(title: str, description: str) -> None:
    name = title.lower().replace(' ', '_')
    directory = Path(__file__).parent.parent / 'examples' / name
    content = [p for p in directory.glob('*') if p.name != '__pycache__' and not p.name.startswith('.')]
    filename = 'main.py' if len(content) == 1 else ''
    with ui.link(target=f'https://github.com/zauberzeug/nicegui/tree/main/examples/{name}/{filename}') \
            .classes('bg-[#5898d420] p-4 self-stretch rounded flex flex-col gap-2') \
            .style('box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1)'):
        ui.label(title).classes(replace='font-bold')
        ui.markdown(description).classes(replace='bold-links arrow-links')


def features(icon: str, title: str, items: List[str]) -> None:
    with ui.column().classes('gap-1'):
        ui.icon(icon).classes('max-sm:hidden text-3xl md:text-5xl mb-3 text-primary opacity-80')
        ui.label(title).classes('font-bold mb-3')
        for item in items:
            ui.markdown(f'- {item}').classes('bold-links arrow-links')


def side_menu() -> ui.left_drawer:
    return ui.left_drawer() \
        .classes('column no-wrap gap-1 bg-[#eee] dark:bg-[#1b1b1b] mt-[-20px] px-8 py-20') \
        .style('height: calc(100% + 20px) !important')
