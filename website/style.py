from typing import List

from nicegui import ui


def header_link(title: str, target: str) -> ui.link:
    return ui.link(title, target).classes(replace='text-lg text-white')


def link_target(name: str, offset: str = '0') -> ui.link_target:
    target = ui.link_target(name).style(f'position: absolute; top: {offset}; left: 0')
    target.parent_slot.parent.classes('relative')
    return target


def section_heading(subtitle: str, title: str) -> None:
    ui.label(subtitle).classes('text-lg text-bold')
    ui.markdown(title).classes('text-5xl font-medium mt-[-12px]')


def heading(title: str) -> ui.label:
    return ui.label(title).classes('text-5xl font-medium text-white')


def title(content: str) -> ui.markdown:
    return ui.markdown(content).classes('text-4xl sm:text-5xl md:text-6xl font-medium')


def subtitle(content: str) -> ui.markdown:
    return ui.markdown(content).classes('text-xl sm:text-2xl md:text-3xl leading-7')


def example_link(title: str, description: str) -> None:
    name = title.lower().replace(' ', '_')
    with ui.column().classes('gap-0'):
        with ui.link(target=f'https://github.com/zauberzeug/nicegui/tree/main/examples/{name}/main.py'):
            ui.label(title).classes(replace='text-black text-bold')
            ui.markdown(description).classes(replace='text-black bold-links')


def features(icon: str, title: str, items: List[str]) -> None:
    with ui.column().classes('gap-1 col-3'):
        ui.icon(icon).classes('text-5xl mb-3 text-primary opacity-80')
        ui.label(title).classes('text-bold mb-3')
        for item in items:
            ui.markdown(f'- {item}').classes('bold-links')
