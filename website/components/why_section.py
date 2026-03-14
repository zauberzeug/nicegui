from nicegui import ui

from .shared import section, section_heading

TIMELINE_STEPS = [
    ('Streamlit', 'Great for quick dashboards, but implicit re-runs make complex state tricky.', False),
    ('JustPy', 'Right idea \u2014 components in Python \u2014 but too bare-bones for production UIs.', False),
    ('NiceGUI', 'Explicit state, rich components, and batteries included \u2014 the sweet spot.', True),
]


def _timeline_step(name: str, description: str, *, active: bool = False) -> None:
    """Render a single step in the Why timeline."""
    classes = 'mo-why-timeline-step'
    if active:
        classes += ' mo-why-timeline-step-active'
    with ui.column().classes(classes):
        ui.element('div').classes('mo-why-timeline-dot')
        ui.label(name).classes('font-semibold')
        ui.label(description).classes('mo-why-timeline-desc')


def create() -> None:
    """Create the Why section with pull-quote, timeline, and tech stack."""
    with section('why', offset='70px'):
        section_heading('why', 'Why?', center=True)

        with ui.column().classes('mo-why-inner mo-reveal'):
            ui.label(
                '\u201cWe liked Streamlit but found it does too much magic '
                'when it comes to state handling.\u201d'
            ).classes('mo-why-pullquote')

            with ui.row().classes('mo-why-timeline'):
                for i, (name, desc, active) in enumerate(TIMELINE_STEPS):
                    if i > 0:
                        ui.element('div').classes('mo-why-timeline-connector')
                    _timeline_step(name, desc, active=active)

            ui.markdown('''
                Built with [Vue](https://vuejs.org/) and [Quasar](https://quasar.dev/) on the frontend,
                [FastAPI](https://fastapi.tiangolo.com/), [Starlette](https://www.starlette.io/),
                and [Uvicorn](https://www.uvicorn.org/) under the hood.
            ''').classes('mo-why-techstack bold-links')
