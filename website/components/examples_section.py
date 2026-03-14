from nicegui import ui

from ..examples import Example, examples
from ..style import link_target

# Examples to feature on the main page
FEATURED_TITLES = {'Authentication', 'Chat App', 'Todo List'}


def _example_card(example: Example) -> None:
    """Render a single example card with image, title, and description."""
    with ui.link(target=example.url).classes('mo-example-card'):
        with ui.element('div').classes('mo-example-img-wrap'):
            ui.interactive_image(example.screenshot).classes('mo-example-img')
        with ui.element('div').classes('mo-example-body'):
            ui.html(f'<h3>{example.title}</h3>', sanitize=False)
            ui.html(f'<p>{example.description}</p>', sanitize=False)


def create() -> None:
    """Create the examples section with featured example cards."""
    with ui.element('section').classes('mo-section').props('id=examples'):
        link_target('examples')
        with ui.element('div').classes('mo-reveal'):
            ui.html('<div class="mo-section-label">examples</div>', sanitize=False)
            ui.html('<h2 class="mo-section-title">Built with NiceGUI.</h2>', sanitize=False)
            ui.html(
                '<p class="mo-section-desc">Real-world examples you can learn from and adapt.</p>',
                sanitize=False,
            )

        with ui.element('div').classes('mo-examples-grid mo-reveal'):
            for example in examples:
                if example.title in FEATURED_TITLES:
                    _example_card(example)

        ui.link('Browse all examples \u2192', '/examples') \
            .classes('mo-examples-cta mo-reveal')
