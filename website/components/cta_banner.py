from nicegui import ui


def create() -> None:
    """Create the CTA banner between demos and examples."""
    with ui.element('div').classes('mo-cta-banner mo-reveal'):
        ui.html('<h2 class="mo-cta-banner-title">Browse through plenty of live demos.</h2>', sanitize=False)
        ui.html(
            '<p class="mo-cta-banner-subtitle">'
            'Fun-Fact: This whole website is also coded with NiceGUI.'
            '</p>',
            sanitize=False,
        )
        ui.link('Documentation', '/documentation') \
            .classes('mo-btn-primary').style('color: white !important')
