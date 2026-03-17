from nicegui import ui

from .shared import section, section_heading

TIMELINE_STEPS = [
    ('Streamlit', 'Great for quick dashboards, but implicit re-runs make complex state tricky.', False),
    ('JustPy', 'Right idea \u2014 components in Python \u2014 but too bare-bones for production UIs.', False),
    ('NiceGUI', 'Explicit state, rich components, and batteries included \u2014 the sweet spot.', True),
]


def _timeline_step(name: str, description: str, *, active: bool = False) -> None:
    """Render a single step in the Why timeline."""
    active_cls = ' mo-why-timeline-step-active' if active else ''
    with ui.column().classes(
        f'mo-why-timeline-step flex-1 flex flex-col items-center gap-3 text-center px-4{active_cls}'
    ):
        dot_style = (
            'border-color: var(--mo-brand-blue); background: var(--mo-brand-blue);'
            ' box-shadow: 0 0 8px color-mix(in srgb, var(--mo-brand-blue) 40%, transparent)'
            if active else
            'background: var(--mo-surface); border: 2px solid var(--mo-text-muted)'
        )
        ui.element('div').classes(
            'mo-why-timeline-dot w-3.5 h-3.5 rounded-full shrink-0 z-10'
        ).style(dot_style)
        ui.label(name).classes('font-semibold')
        ui.label(description).classes(
            'text-sm leading-normal max-w-[240px]'
        ).style('color: var(--mo-text-secondary)')


def create() -> None:
    """Create the Why section with pull-quote, timeline, and tech stack."""
    with section('why', offset='70px'):
        section_heading('why', 'Why?', center=True)

        with ui.column().classes(
            'mo-reveal max-w-[860px] mx-auto text-center flex flex-col items-center gap-6'
        ):
            ui.label(
                '\u201cWe liked Streamlit but found it does too much magic '
                'when it comes to state handling.\u201d'
            ).classes(
                'text-[1.1875rem] italic leading-relaxed text-center max-w-[640px] mb-4'
            ).style('color: var(--mo-text-secondary)')

            with ui.row().classes(
                'mo-why-timeline flex items-start w-full my-4'
            ):
                for i, (name, desc, active) in enumerate(TIMELINE_STEPS):
                    if i > 0:
                        ui.element('div').classes(
                            'mo-why-timeline-connector w-12 h-0.5 shrink-0 mt-[6px]'
                        ).style('background: var(--mo-border)')
                    _timeline_step(name, desc, active=active)

            ui.markdown('''
                Built with [Vue](https://vuejs.org/) and [Quasar](https://quasar.dev/) on the frontend,
                [FastAPI](https://fastapi.tiangolo.com/), [Starlette](https://www.starlette.io/),
                and [Uvicorn](https://www.uvicorn.org/) under the hood.
            ''').classes('bold-links text-[0.9375rem] leading-relaxed mt-2').style(
                'color: var(--mo-text-secondary)'
            )
