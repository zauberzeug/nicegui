from nicegui import ui

from .components import (
    SCROLL_REVEAL_JS,
    about_section,
    cta_section,
    demos_section,
    examples_section,
    features_section,
    footer_section,
    hero_section,
    installation_section,
    sponsors_section,
    why_section,
)


def create() -> None:
    """Create the content of the main page."""
    ui.add_head_html(SCROLL_REVEAL_JS)
    ui.context.client.content.classes('mo-page')
    ui.run_javascript('document.querySelector(".q-layout").classList.add("mo-header-transparent")')

    hero_section.create()
    about_section.create()
    installation_section.create()
    features_section.create()
    demos_section.create()
    cta_section.create()
    examples_section.create()
    sponsors_section.create()
    why_section.create()
    footer_section.create()
