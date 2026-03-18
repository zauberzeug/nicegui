from nicegui import ui

from .shared import section


def create() -> None:
    """Create the CTA banner between demos and examples."""
    with section('cta'):
        with ui.column().classes('mo-reveal w-full items-center text-center gap-0'):
            ui.label('Browse through plenty of live demos.') \
                .classes('text-[clamp(1.5rem,2.5vw,2.25rem)] font-semibold tracking-tight mb-2 text-(--mo-text-primary)')
            ui.label('Fun-Fact: This whole website is also coded with NiceGUI.') \
                .classes('text-lg mb-8 text-(--mo-text-secondary)')
            ui.link('Documentation', '/documentation').classes(
                'mo-btn-primary inline-flex items-center gap-2 px-7 py-3 rounded-full'
                ' font-medium text-base cursor-pointer no-underline w-auto'
                ' transition-all duration-150 hover:-translate-y-px'
            ).style(
                'background: var(--mo-brand-blue); color: #fff;'
                ' box-shadow: 0 2px 8px color-mix(in srgb, var(--mo-brand-blue) 30%, transparent)'
            )
