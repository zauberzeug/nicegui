from nicegui import ui

from ..examples import Example, examples
from .shared import section, section_heading

FEATURED_TITLES = {'Authentication', 'Chat App', 'Todo List'}


def create() -> None:
    """Create the examples section with featured example cards."""
    with section('examples'):
        section_heading('examples', 'Built with NiceGUI.',
                        'Real-world examples you can learn from and adapt.')

        with ui.element().classes('mo-reveal grid grid-cols-3 gap-6 max-lg:grid-cols-2 max-sm:grid-cols-1'):
            for example in examples:
                if example.title in FEATURED_TITLES:
                    _example_card(example)

        ui.link('Browse all examples \u2192', '/examples') \
            .classes('mo-reveal mt-8 font-medium no-underline inline-flex items-center gap-1 hover:underline w-auto text-(--mo-brand-blue)')


def _example_card(example: Example) -> None:
    """Render a single example card with screenshot, title, and description."""
    with ui.link(target=example.url).classes(
        'rounded-2xl overflow-hidden no-underline transition-all duration-200 cursor-pointer hover:-translate-y-0.5'
    ).style('background: var(--mo-surface); border: 1px solid var(--mo-border)'):
        with ui.element().classes('overflow-hidden aspect-video bg-white p-4'):
            ui.interactive_image(example.screenshot) \
                .classes('w-full h-full object-cover transition-transform duration-300')
        with ui.column().classes('p-5'):
            ui.label(example.title).classes('text-lg font-semibold mb-1')
            ui.label(example.description).classes('text-sm leading-normal mb-3 text-(--mo-text-secondary)')
