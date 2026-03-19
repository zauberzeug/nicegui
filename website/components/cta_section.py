from nicegui import ui

from .shared import cta_button, section


def create() -> None:
    """Create the CTA banner between demos and examples."""
    with section('cta'):
        with ui.column().classes('mo-reveal w-full items-center text-center gap-0'):
            ui.label('Browse through plenty of live demos.') \
                .classes('text-[clamp(1.5rem,2.5vw,2.25rem)] font-semibold tracking-tight mb-2 text-(--mo-text-primary)')
            ui.label('Fun-Fact: This whole website is also coded with NiceGUI.') \
                .classes('text-lg mb-8 text-(--mo-text-secondary)')
            cta_button('Documentation', on_click=lambda: ui.navigate.to('/documentation'))
