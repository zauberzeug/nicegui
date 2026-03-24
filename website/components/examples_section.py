from nicegui import ui

from .. import design as d
from ..examples import Example, examples
from .shared import section, section_heading

FEATURED_TITLES = {'Authentication', 'Chat App', 'Todo List'}


def create() -> None:
    """Create the examples section with featured example cards."""
    with section('examples'):
        section_heading('examples', 'Built with NiceGUI.',
                        'Real-world examples you can learn from and adapt.')

        with ui.element().classes('reveal grid grid-cols-3 gap-6 max-lg:grid-cols-2 max-sm:grid-cols-1'):
            for example in examples:
                if example.title in FEATURED_TITLES:
                    example_card(example)

        ui.link('Browse all examples \u2192', '/examples') \
            .classes(f'reveal mt-8 font-medium no-underline inline-flex items-center gap-1 hover:underline w-auto {d.TEXT_BLUE}')


def example_card(example: Example) -> None:
    """Render a single example card with screenshot, title, and description."""
    with ui.link(target=example.url).classes(
        'rounded-2xl overflow-hidden no-underline transition-all duration-200 cursor-pointer hover:-translate-y-0.5'
        f' {d.BG_SURFACE} {d.BORDER} hover:{d.BORDER_ACCENT}'
    ):
        with ui.element().classes(f'overflow-hidden aspect-video bg-white p-4 dark:brightness-[0.85] {d.BORDER_B}'):
            ui.interactive_image(example.screenshot) \
                .classes('size-full object-cover transition-transform duration-300')
        with ui.column().classes('p-5 gap-1'):
            ui.label(example.title).classes('text-lg font-semibold')
            ui.label(example.description).classes(f'text-sm leading-normal mb-2 {d.TEXT_SECONDARY}')
