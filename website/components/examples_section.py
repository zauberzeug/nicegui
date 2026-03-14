from nicegui import ui

from ..examples import Example, examples
from .shared import section, section_heading

FEATURED_TITLES = {'Authentication', 'Chat App', 'Todo List'}


def _example_card(example: Example) -> None:
    """Render a single example card with screenshot, title, and description."""
    with ui.link(target=example.url).classes('mo-example-card'):
        with ui.element('div').classes('mo-example-img-wrap'):
            ui.interactive_image(example.screenshot).classes('mo-example-img')
        with ui.column().classes('mo-example-body'):
            ui.label(example.title).classes('text-lg font-semibold mb-1')
            ui.label(example.description).classes('text-sm').style('color: var(--mo-text-secondary)')


def create() -> None:
    """Create the examples section with featured example cards."""
    with section('examples'):
        section_heading('examples', 'Built with NiceGUI.',
                        'Real-world examples you can learn from and adapt.')

        with ui.element('div').classes('mo-examples-grid mo-reveal'):
            for example in examples:
                if example.title in FEATURED_TITLES:
                    _example_card(example)

        ui.link('Browse all examples \u2192', '/examples').classes('mo-examples-cta mo-reveal')
