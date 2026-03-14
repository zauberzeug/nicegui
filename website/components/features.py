from nicegui import ui

from ..style import link_target

FEATURE_DATA = [
    {
        'icon': 'swap_horiz',
        'title': 'Interaction',
        'items': [
            'Buttons, switches, sliders, inputs and more',
            'Notifications, dialogs and menus',
            'Interactive images with SVG overlays',
            'Web pages and native window apps',
        ],
    },
    {
        'icon': 'space_dashboard',
        'title': 'Layout',
        'items': [
            'Navigation bars, tabs, panels',
            'Rows, columns, grids and cards',
            'HTML and Markdown elements',
            'Flex layout by default',
        ],
    },
    {
        'icon': 'insights',
        'title': 'Visualization',
        'items': [
            'Charts, diagrams, tables, audio/video',
            '3D scenes',
            'Straight-forward data binding',
            'Built-in timer for data refresh',
        ],
    },
    {
        'icon': 'brush',
        'title': 'Styling',
        'items': [
            'Customizable color themes',
            'Custom CSS and classes',
            'Modern look with material design',
            'Tailwind CSS',
        ],
    },
    {
        'icon': 'source',
        'title': 'Coding',
        'items': [
            'Single page apps with ui.sub_pages',
            'Auto-reload on code change',
            'Persistent user sessions',
            'Super powerful testing framework',
        ],
    },
    {
        'icon': 'anchor',
        'title': 'Foundation',
        'items': [
            'Generic Vue to Python bridge',
            'Dynamic GUI through Quasar',
            'Content served with FastAPI',
            'Python 3.10+',
        ],
    },
]


def _bento_card(icon: str, title: str, items: list[str]) -> None:
    """Render a single bento feature card."""
    with ui.element('div').classes('mo-bento-card'):
        ui.icon(icon).classes('mo-bento-icon')
        ui.html(f'<h3>{title}</h3>', sanitize=False)
        items_html = ''.join(f'<li>{item}</li>' for item in items)
        ui.html(f'<ul>{items_html}</ul>', sanitize=False)


def create() -> None:
    """Create the features section with bento grid cards."""
    with ui.element('section').classes('mo-section').props('id=features'):
        link_target('features')
        with ui.element('div').classes('mo-reveal'):
            ui.html('<div class="mo-section-label">features</div>', sanitize=False)
            ui.html('<h2 class="mo-section-title">Code nicely.</h2>', sanitize=False)
            ui.html(
                '<p class="mo-section-desc">'
                'Everything you need to build sophisticated web UIs, all from Python.'
                '</p>',
                sanitize=False,
            )

        with ui.element('div').classes('mo-bento-grid mo-reveal'):
            for feature in FEATURE_DATA:
                _bento_card(feature['icon'], feature['title'], feature['items'])
