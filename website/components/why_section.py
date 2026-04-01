from nicegui import ui

from .. import design as d
from ..design import phosphor_icon
from .shared import section, section_heading


def create() -> None:
    """Create the Why section with pull-quote and value propositions."""
    with section('why'):
        section_heading('', 'Why?', center=True)

        with ui.column(align_items='center').classes('reveal gap-2 self-center text-center mt-6'):
            ui.label('\u201cWe like Streamlit but find it does too much magic when it comes to state handling.\u201d') \
                .classes(f'italic {d.TEXT_19PX} leading-relaxed {d.TEXT_SECONDARY} max-w-[480px]')
            ui.link('Read the full story \u2192', 'https://github.com/zauberzeug/nicegui/discussions/21') \
                .classes(f'{d.TEXT_15PX} {d.TEXT_BLUE}!')

        with ui.row(wrap=False).classes('reveal gap-0 w-full mt-10 max-md:flex-col max-md:items-center'):
            _pillar('ph-file-py', 'Just Python',
                    'No HTML, CSS, or JavaScript needed. Build web interfaces entirely in Python '
                    'using familiar patterns and your existing tooling.')
            ui.element().classes('w-px self-stretch bg-gray-500/15 max-md:hidden')
            _pillar('ph-trend-up', 'Grows with You',
                    'From a 10-line prototype to a multi-page production app \u2014 '
                    'same patterns, same codebase, no rewrite needed.')
            ui.element().classes('w-px self-stretch bg-gray-500/15 max-md:hidden')
            _pillar('ph-battery-full', 'Batteries Included',
                    '100+ components, reactive data binding, charts & plots, 3D\u00a0scenes, native desktop apps, '
                    'and Docker support \u2014 all out of the box.')

        ui.markdown('''
            Built with [Vue](https://vuejs.org/) and [Quasar](https://quasar.dev/) on the frontend,
            [FastAPI](https://fastapi.tiangolo.com/), [Starlette](https://www.starlette.io/),
            and [Uvicorn](https://www.uvicorn.org/) under the hood.
            [Learn more →](/documentation/section_foundations)
        ''').classes(f'reveal self-center text-center {d.TEXT_15PX} leading-relaxed mt-10 {d.TEXT_SECONDARY}')


def _pillar(icon: str, title: str, description: str) -> None:
    """Render a single value proposition pillar."""
    with ui.column(align_items='center').classes('gap-3 flex-1 px-8 py-4 text-center'):
        phosphor_icon(icon).classes(f'text-3xl {d.TEXT_BLUE}')
        ui.label(title).classes(f'{d.TEXT_19PX} font-semibold {d.TEXT_PRIMARY}')
        ui.label(description).classes(f'{d.TEXT_15PX} leading-relaxed {d.TEXT_SECONDARY}')
