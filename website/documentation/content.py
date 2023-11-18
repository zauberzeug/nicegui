from typing import Dict

from .section import Section
from .sections import (action_events, audiovisual_elements, binding_properties, configuration_deployment, controls,
                       data_elements, page_layout, styling_appearance, text_elements)
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
        configuration_deployment,
    ]
}


def create_overview() -> None:
    for section in SECTIONS.values():
        section.intro()


def create_section(name: str) -> None:
    section = SECTIONS[name]
    heading(section.title)
    section.content()
