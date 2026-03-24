from nicegui import ui

from .. import design as d
from .shared import cta_button, section


def create() -> None:
    """Create the CTA banner between demos and examples."""
    with section('cta'):
        with ui.column().classes('reveal w-full items-center text-center gap-0'):
            ui.label('Browse through plenty of live demos.') \
                .classes(f'{d.TEXT_CTA_TITLE} font-semibold tracking-tight mb-2 {d.TEXT_PRIMARY}')
            ui.label('Fun-Fact: This whole website is also made with NiceGUI.') \
                .classes(f'{d.TEXT_19PX} mb-8 {d.TEXT_SECONDARY}')
            cta_button('Documentation', on_click=lambda: ui.navigate.to('/documentation'))
