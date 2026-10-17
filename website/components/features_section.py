from nicegui import ui

from .. import design as d
from ..design import phosphor_icon
from ..i18n import t
from .shared import section, section_heading


def create() -> None:
    """Create the features section with grid cards."""
    with section('features'):
        section_heading('features', t('Code nicely.'),
                        t('Everything you need to build sophisticated web UIs, all from Python.'))

        with ui.grid().classes('reveal w-full grid-cols-3 gap-6 max-lg:grid-cols-2 max-sm:grid-cols-1'):
            _card('ph-arrows-left-right', t('Interaction'), [
                t('[Buttons](/documentation/button), [switches](/documentation/switch), '
                  '[sliders](/documentation/slider), [inputs](/documentation/input), ...'),
                t('[Notifications](/documentation/notification), [dialogs](/documentation/dialog) '
                  'and [menus](/documentation/menu)'),
                t('[Interactive images](/documentation/interactive_image) with SVG overlays'),
                t('Web pages and [native window apps](/documentation/section_configuration_deployment#native_mode)'),
            ])
            _card('ph-layout', t('Layout'), [
                t('[Navigation bars](/documentation/page_layout), [tabs](/documentation/tabs), '
                  '[panels](/documentation/expansion)'),
                t('[Rows](/documentation/row), [columns](/documentation/column), '
                  '[grids](/documentation/grid) and [cards](/documentation/card)'),
                t('[HTML](/documentation/html) and [Markdown](/documentation/markdown) elements'),
                t('Flex layout by default'),
            ])
            _card('ph-chart-line-up', t('Visualization'), [
                t('[Charts](/documentation/echart), [tables](/documentation/table), '
                  '[audio](/documentation/audio)/[video](/documentation/video)'),
                t('[3D scenes](/documentation/scene)'),
                t('Straight-forward [data binding](/documentation/section_binding_properties)'),
                t('Built-in [timer](/documentation/timer) for data refresh'),
            ])
            _card('ph-paint-brush', t('Styling'), [
                t('Customizable [color themes](/documentation/section_styling_appearance#color_theming)'),
                t('Custom CSS and classes'),
                t('Modern look with material design'),
                '[Tailwind CSS](https://tailwindcss.com/)',
            ])
            _card('ph-code', t('Coding'), [
                t('Single page apps with [ui.sub_pages](/documentation/sub_pages)'),
                t('Auto-reload on code change'),
                t('Persistent [user sessions](/documentation/storage)'),
                t('Super powerful [testing framework](/documentation/section_testing)'),
            ])
            _card('ph-anchor', t('Foundation'), [
                t('Generic [Vue](https://vuejs.org/) to Python bridge'),
                t('Dynamic GUI through [Quasar](https://quasar.dev/)'),
                t('Content served with [FastAPI](https://fastapi.tiangolo.com/)'),
                'Python 3.10+',
            ])


def _card(icon: str, title: str, items: list[str]) -> None:
    """Render a single feature card with icon, title, and bullet list."""
    with ui.column().classes(f'relative rounded-2xl p-7 gap-0 group transition-transform duration-200 cursor-default hover:-translate-y-0.5 {d.BG_SURFACE} {d.BORDER}'):
        ui.label('ui.card()') \
            .classes(f'absolute top-2.5 right-3 font-mono {d.TEXT_13PX} {d.TEXT_BLUE} opacity-0 group-hover:opacity-30 transition-opacity duration-300 pointer-events-none')
        phosphor_icon(icon) \
            .classes(f'{d.TEXT_32PX} {d.TEXT_BLUE} [&_i::before]:text-[{d.ACCENT}] [&_i::before]:!opacity-40 [&_i::after]:relative')
        ui.label(title).classes(f'{d.TEXT_19PX} font-semibold mb-3 tracking-tight').props('role=heading aria-level=3')
        ui.markdown('\n'.join(f'- {item}' for item in items)) \
            .classes(f'{d.TEXT_15PX} leading-7 {d.TEXT_SECONDARY} [&_ul]:pl-4 [&_li]:pl-1 [&_li]:marker:{d.TEXT_BLUE}/50')
