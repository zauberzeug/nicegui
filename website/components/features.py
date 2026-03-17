from nicegui import ui

from .shared import section, section_heading

FEATURES = [
    ('ph-arrows-left-right', 'Interaction', [
        'Buttons, switches, sliders, inputs and more',
        'Notifications, dialogs and menus',
        'Interactive images with SVG overlays',
        'Web pages and native window apps',
    ]),
    ('ph-layout', 'Layout', [
        'Navigation bars, tabs, panels',
        'Rows, columns, grids and cards',
        'HTML and Markdown elements',
        'Flex layout by default',
    ]),
    ('ph-chart-line-up', 'Visualization', [
        'Charts, diagrams, tables, audio/video',
        '3D scenes',
        'Straight-forward data binding',
        'Built-in timer for data refresh',
    ]),
    ('ph-paint-brush', 'Styling', [
        'Customizable color themes',
        'Custom CSS and classes',
        'Modern look with material design',
        'Tailwind CSS',
    ]),
    ('ph-code', 'Coding', [
        'Single page apps with ui.sub_pages',
        'Auto-reload on code change',
        'Persistent user sessions',
        'Super powerful testing framework',
    ]),
    ('ph-anchor', 'Foundation', [
        'Generic Vue to Python bridge',
        'Dynamic GUI through Quasar',
        'Content served with FastAPI',
        'Python 3.10+',
    ]),
]


def _bento_card(icon: str, title: str, items: list[str]) -> None:
    """Render a single bento feature card with icon, title, and bullet list."""
    with ui.column().classes(
        'mo-bento-card relative overflow-hidden rounded-2xl p-7'
        ' transition-all duration-200 cursor-default'
        ' hover:-translate-y-0.5'
    ).style(
        'background: var(--mo-surface); border: 1px solid var(--mo-border)'
    ):
        ui.html(f'<i class="ph-duotone {icon}"></i>', sanitize=False).classes(
            'text-[2rem] mb-4'
        ).style('color: var(--mo-brand-blue)')
        ui.label(title).classes('text-xl font-semibold mb-3 tracking-tight')
        with ui.column().classes('gap-1.5'):
            for item in items:
                with ui.row().classes('items-start gap-3'):
                    ui.element('span').classes(
                        'w-[5px] h-[5px] rounded-full shrink-0 mt-[9px] opacity-50'
                    ).style('background: var(--mo-brand-blue)')
                    ui.label(item).classes(
                        'text-[0.9375rem] leading-normal'
                    ).style('color: var(--mo-text-secondary)')


def create() -> None:
    """Create the features section with bento grid cards."""
    with section('features'):
        section_heading('features', 'Code nicely.',
                        'Everything you need to build sophisticated web UIs, all from Python.')

        with ui.element('div').classes(
            'mo-reveal grid grid-cols-3 gap-6 max-lg:grid-cols-2 max-sm:grid-cols-1'
        ):
            for icon, title, items in FEATURES:
                _bento_card(icon, title, items)
