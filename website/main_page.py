from nicegui import ui

from .components import (
    SCROLL_REVEAL_JS,
    about,
    cta_banner,
    demos,
    examples_section,
    features,
    footer,
    hero,
    installation,
    sponsors_section,
    why_section,
)


def create() -> None:
    """Create the content of the main page."""
    ui.add_head_html(SCROLL_REVEAL_JS)
    ui.context.client.content.classes('mo-page')
    ui.run_javascript('document.querySelector(".q-layout").classList.add("mo-header-transparent")')

    hero.create()
    about.create()
    installation.create()
    features.create()
    demos.create()
    cta_banner.create()
    examples_section.create()
    sponsors_section.create()
    why_section.create()
    footer.create()
