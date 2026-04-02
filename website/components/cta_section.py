from nicegui import ui

from .. import design as d
from .shared import cta_button, section


def create() -> None:
    """Create the CTA banner between demos and examples."""
    with section('cta'):
        with ui.column(align_items='center') \
                .classes(f'reveal w-full text-center gap-0 {d.BG_BLUE}/25 rounded-xl py-16 max-sm:px-6 min-sm:px-16 {d.SHADOW_CARD}'):
            ui.label('Browse through plenty of live demos.') \
                .classes(f'{d.TEXT_CTA_TITLE} font-semibold tracking-tight mb-2 {d.TEXT_PRIMARY}')
            ui.label('Fun-Fact: This whole website is also made with NiceGUI.') \
                .classes(f'{d.TEXT_19PX} mb-8 {d.TEXT_SECONDARY}')
            cta_button('Documentation', on_click=lambda: ui.navigate.to('/documentation')).classes('mb-12')
            ui.markdown('''
                **Or, let your AI do it!**
                Most LLMs already know NiceGUI, and
                our [documentation index](/documentation/section_configuration_deployment#documentation_index)
                puts the full API into a single JSON file.
            ''').classes(f'{d.TEXT_15PX} {d.TEXT_SECONDARY} max-w-120')
