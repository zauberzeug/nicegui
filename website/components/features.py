from nicegui import ui

from .shared import section, section_heading

FEATURES = [
    ('swap_horiz', 'Interaction', [
        'Buttons, switches, sliders, inputs and more',
        'Notifications, dialogs and menus',
        'Interactive images with SVG overlays',
        'Web pages and native window apps',
    ]),
    ('space_dashboard', 'Layout', [
        'Navigation bars, tabs, panels',
        'Rows, columns, grids and cards',
        'HTML and Markdown elements',
        'Flex layout by default',
    ]),
    ('insights', 'Visualization', [
        'Charts, diagrams, tables, audio/video',
        '3D scenes',
        'Straight-forward data binding',
        'Built-in timer for data refresh',
    ]),
    ('brush', 'Styling', [
        'Customizable color themes',
        'Custom CSS and classes',
        'Modern look with material design',
        'Tailwind CSS',
    ]),
    ('source', 'Coding', [
        'Single page apps with ui.sub_pages',
        'Auto-reload on code change',
        'Persistent user sessions',
        'Super powerful testing framework',
    ]),
    ('anchor', 'Foundation', [
        'Generic Vue to Python bridge',
        'Dynamic GUI through Quasar',
        'Content served with FastAPI',
        'Python 3.10+',
    ]),
]


def _bento_card(icon: str, title: str, items: list[str]) -> None:
    """Render a single bento feature card with icon, title, and bullet list."""
    with ui.column().classes('mo-bento-card'):
        ui.icon(icon).classes('mo-bento-icon')
        ui.label(title).classes('text-xl font-semibold mb-3')
        for item in items:
            ui.label(item).classes('mo-bento-card-item')


def create() -> None:
    """Create the features section with bento grid cards."""
    with section('features'):
        section_heading('features', 'Code nicely.',
                        'Everything you need to build sophisticated web UIs, all from Python.')

        with ui.element('div').classes('mo-bento-grid mo-reveal'):
            for icon, title, items in FEATURES:
                _bento_card(icon, title, items)
