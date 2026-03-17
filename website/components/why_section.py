from nicegui import ui

from .shared import section, section_heading


def create() -> None:
    """Create the Why section with pull-quote, timeline, and tech stack."""
    with section('why'):
        section_heading('why', 'Why?', center=True)

        with ui.column().classes('mo-reveal max-w-[860px] mx-auto text-center flex flex-col items-center gap-6'):
            ui.label('\u201cWe liked Streamlit but found it does too much magic '
                     'when it comes to state handling.\u201d') \
                .classes('text-[1.1875rem] italic leading-relaxed text-center max-w-[640px] mb-4') \
                .style('color: var(--mo-text-secondary)')

            with ui.row(wrap=False).classes('max-sm:flex-col max-sm:items-center'):
                _step('Streamlit', 'Great for quick dashboards, but implicit re-runs make complex state tricky.')
                _separator()
                _step('JustPy', 'Right idea \u2014 components in Python \u2014 but too bare-bones for production UIs.')
                _separator()
                _step('NiceGUI', 'Explicit state, rich components, and batteries included \u2014 the sweet spot.', True)

            ui.markdown('''
                Built with [Vue](https://vuejs.org/) and [Quasar](https://quasar.dev/) on the frontend,
                [FastAPI](https://fastapi.tiangolo.com/), [Starlette](https://www.starlette.io/),
                and [Uvicorn](https://www.uvicorn.org/) under the hood.
            ''').classes('bold-links text-[0.9375rem] leading-relaxed mt-2 text-(--mo-text-secondary)')


def _step(name: str, description: str, active: bool = False) -> None:
    """Render a single step in the Why timeline."""
    with ui.column(align_items='center').classes('gap-3'):
        ui.element().classes('size-3.5 rounded-full') \
            .classes('bg-primary' if active else 'border-2  border-(--mo-border)')
        ui.label(name).classes('font-semibold')
        ui.label(description).classes('text-sm leading-normal max-w-[240px] text-(--mo-text-secondary)')


def _separator() -> None:
    """Render the separator line between steps in the Why timeline."""
    ui.element().classes('m-2 w-12 h-0.5 max-sm:w-0.5 max-sm:h-4 bg-(--mo-border)')
