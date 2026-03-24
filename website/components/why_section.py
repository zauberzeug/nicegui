from nicegui import ui

from .. import design as d
from .shared import section, section_heading


def create() -> None:
    """Create the Why section with pull-quote, timeline, and tech stack."""
    with section('why'):
        section_heading('why', 'Why?', center=True)

        with ui.row(wrap=False).classes('reveal py-8 self-center text-center max-sm:flex-col max-sm:items-center'):
            _step(0, 'Streamlit', 'Great for quick dashboards, but implicit re-runs make complex state tricky.')
            _separator()
            _step(1, 'JustPy', 'Right idea \u2014 components in Python \u2014 but too bare-bones for production UIs.')
            _separator()
            _step(2, 'NiceGUI', 'Explicit state, rich components, and batteries included \u2014 the sweet spot.')

        ui.markdown('''
            Built with [Vue](https://vuejs.org/) and [Quasar](https://quasar.dev/) on the frontend,
            [FastAPI](https://fastapi.tiangolo.com/), [Starlette](https://www.starlette.io/),
            and [Uvicorn](https://www.uvicorn.org/) under the hood.
        ''').classes(f'reveal self-center text-center {d.TEXT_15PX} leading-relaxed mt-2 {d.TEXT_SECONDARY}')


def _step(number: int, name: str, description: str) -> None:
    """Render a single step in the Why timeline."""
    with ui.column(align_items='center').classes('gap-3'):
        dot = ui.element().classes('size-3.5 rounded-full')
        if number == 2:
            dot.classes(d.BG_BLUE).style(f'box-shadow: 0 0 8px color-mix(in srgb, {d.BLUE} 40%, transparent)')
        else:
            dot.classes('border-2 border-gray-500/50')
        ui.label(name).classes(f'{d.TEXT_19PX} font-semibold')
        ui.label(description).classes(f'{d.TEXT_15PX} leading-normal max-w-[240px] {d.TEXT_SECONDARY}')


def _separator() -> None:
    """Render the separator line between steps in the Why timeline."""
    ui.element().classes('m-2 w-12 h-0.5 max-sm:w-0.5 max-sm:h-4 bg-gray-500/15')
