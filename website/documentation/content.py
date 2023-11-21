from typing import Dict

from nicegui import ui

from .section import Section
from .sections import (action_events, audiovisual_elements, binding_properties, configuration_deployment, controls,
                       data_elements, page_layout, pages_routing, styling_appearance, text_elements)
from .tools import heading

SECTIONS: Dict[str, Section] = {
    section.name: section
    for section in [
        text_elements,
        controls,
        audiovisual_elements,
        data_elements,
        binding_properties,
        page_layout,
        styling_appearance,
        action_events,
        pages_routing,
        configuration_deployment,
    ]
}


def create_overview() -> None:
    with ui.grid().classes('grid-cols-[1fr] md:grid-cols-[1fr_1fr] xl:grid-cols-[1fr_1fr_1fr]'):
        for section in SECTIONS.values():
            with ui.link(target=f'/documentation/section_{section.name}/') \
                    .classes('bg-[#5898d420] p-4 self-stretch rounded flex flex-col gap-2') \
                    .style('box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1)'):
                ui.label(section.title).classes(replace='text-2xl')
                ui.markdown(section.description).classes(replace='bold-links arrow-links')


def create_section(name: str) -> None:
    section = SECTIONS[name]
    heading(section.title)
    section.content()
