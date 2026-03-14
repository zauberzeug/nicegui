from nicegui import ui

from .shared import section


def create() -> None:
    """Create the CTA banner between demos and examples."""
    with section(classes='mo-cta-banner-bg'):
        with ui.column().classes('mo-reveal items-center text-center'):
            ui.label('Browse through plenty of live demos.').classes('mo-cta-banner-title')
            ui.label('Fun-Fact: This whole website is also coded with NiceGUI.').classes('mo-cta-banner-subtitle')
            ui.link('Documentation', '/documentation').classes('mo-btn-primary')
