from nicegui import ui

from .. import design as d
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
    with ui.column().classes(f'relative rounded-2xl p-7 gap-0 group transition-all duration-200 cursor-default hover:-translate-y-0.5 {d.BG_SURFACE} {d.BORDER}'):
        ui.label('ui.card()') \
            .classes(f'absolute top-2.5 right-3 font-mono {d.TEXT_13PX} {d.TEXT_BRAND_BLUE} opacity-0 group-hover:opacity-30 transition-opacity duration-300 pointer-events-none')
        phosphor_icon(icon).classes(f'{d.TEXT_32PX} {d.TEXT_BRAND_BLUE}')
        ui.label(title).classes('text-xl font-semibold mb-3 tracking-tight')
        ui.markdown('\n'.join(f'- {item}' for item in items)) \
            .classes(f'{d.TEXT_15PX} leading-7 {d.TEXT_SECONDARY} [&_ul]:pl-4 [&_li]:pl-1 [&_li]:marker:{d.TEXT_BRAND_BLUE}/50')
