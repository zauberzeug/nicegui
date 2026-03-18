from nicegui import ui

from ..utils import phosphor_icon
from .shared import section, section_heading


def create() -> None:
    """Create the features section with grid cards."""
    with section('features'):
        section_heading('features', 'Code nicely.',
                        'Everything you need to build sophisticated web UIs, all from Python.')

        with ui.grid().classes('mo-reveal w-full grid-cols-3 gap-6 max-lg:grid-cols-2 max-sm:grid-cols-1'):
            _card('ph-arrows-left-right', 'Interaction', [
                'Buttons, switches, sliders, inputs and more',
                'Notifications, dialogs and menus',
                'Interactive images with SVG overlays',
                'Web pages and native window apps',
            ])
            _card('ph-layout', 'Layout', [
                'Navigation bars, tabs, panels',
                'Rows, columns, grids and cards',
                'HTML and Markdown elements',
                'Flex layout by default',
            ])
            _card('ph-chart-line-up', 'Visualization', [
                'Charts, diagrams, tables, audio/video',
                '3D scenes',
                'Straight-forward data binding',
                'Built-in timer for data refresh',
            ])
            _card('ph-paint-brush', 'Styling', [
                'Customizable color themes',
                'Custom CSS and classes',
                'Modern look with material design',
                'Tailwind CSS',
            ])
            _card('ph-code', 'Coding', [
                'Single page apps with ui.sub_pages',
                'Auto-reload on code change',
                'Persistent user sessions',
                'Super powerful testing framework',
            ])
            _card('ph-anchor', 'Foundation', [
                'Generic Vue to Python bridge',
                'Dynamic GUI through Quasar',
                'Content served with FastAPI',
                'Python 3.10+',
            ])


def _card(icon: str, title: str, items: list[str]) -> None:
    """Render a single feature card with icon, title, and bullet list."""
    with ui.column() \
            .classes('relative rounded-2xl p-7 gap-0 group transition-all duration-200 cursor-default hover:-translate-y-0.5') \
            .style('background: var(--mo-surface); border: 1px solid var(--mo-border)'):
        ui.label('ui.card()') \
            .classes('absolute top-2.5 right-3 font-mono text-[0.6875rem] text-(--mo-brand-blue) opacity-0 group-hover:opacity-30 transition-opacity duration-300 pointer-events-none')
        phosphor_icon(icon).classes('text-[2rem] text-(--mo-brand-blue)')
        ui.label(title).classes('text-xl font-semibold mb-3 tracking-tight')
        ui.markdown('\n'.join(f'- {item}' for item in items)) \
            .classes('text-[0.9375rem] leading-7 text-(--mo-text-secondary) [&_ul]:pl-4 [&_li]:pl-1 [&_li]:marker:text-(--mo-brand-blue)/50')
