from nicegui import ui

from .. import design as d
from ..utils import phosphor_icon


def create() -> None:
    """Create the 4-column footer with brand, links, and bottom bar."""
    with ui.element('footer').classes(f'w-full pt-20 px-6 {d.BG_FOOTER} {d.BORDER_T}'):
        with ui.grid().classes('max-w-[1280px] mx-auto w-full pb-12 gap-12 '
                               'grid-cols-[2fr_1fr_1fr_1fr] max-sm:grid-cols-1'):
            with ui.column().classes('gap-3'):
                ui.markdown('**Nice**GUI').classes('text-lg -mt-3')
                ui.label('The Python-based UI framework that shows up in your browser.') \
                    .classes(f'text-sm leading-normal {d.TEXT_SECONDARY}')
                with ui.row().classes('gap-3 mt-2'):
                    _icon_link('ph-github-logo', 'https://github.com/zauberzeug/nicegui/')
                    _icon_link('ph-discord-logo', 'https://discord.gg/TEpFeAaF4f')
                    _icon_link('ph-reddit-logo', 'https://www.reddit.com/r/nicegui/')

            _column('Resources', [
                ('Documentation', '/documentation'),
                ('Examples', '/examples'),
                ('GitHub', 'https://github.com/zauberzeug/nicegui/'),
                ('PyPI', 'https://pypi.org/project/nicegui/'),
            ])
            _column('Community', [
                ('Discord', 'https://discord.gg/TEpFeAaF4f'),
                ('Contributing', 'https://github.com/zauberzeug/nicegui/blob/main/CONTRIBUTING.md'),
                ('Discussions', 'https://github.com/zauberzeug/nicegui/discussions'),
                ('Sponsors', 'https://github.com/sponsors/zauberzeug'),
            ])
            _column('Legal', [
                ('Imprint', '/imprint_privacy'),
                ('Privacy', '/imprint_privacy'),
            ])

        with ui.row().classes(
            f'max-w-[1280px] mx-auto w-full py-5 justify-between items-center {d.TEXT_13PX} {d.TEXT_MUTED} {d.BORDER_T}'
        ):
            ui.markdown('Made with NiceGUI by [Zauberzeug](https://zauberzeug.com)')
            ui.markdown('\u00a9 2025 [Zauberzeug GmbH](https://zauberzeug.com)')


def _column(title: str, links: list[tuple[str, str]]) -> None:
    """Render a footer link column with heading and list of (label, url) pairs."""
    with ui.column().classes('gap-2.5'):
        ui.label(title).classes(f'text-xs font-semibold uppercase tracking-widest mb-4 {d.TEXT_MUTED}')
        for label, url in links:
            ui.link(label, url).classes(f'{d.TEXT_15PX} no-underline transition-colors duration-150 {d.TEXT_SECONDARY}')


def _icon_link(icon: str, url: str) -> None:
    """Render a circular icon link with hover effect."""
    with ui.link(target=url) \
            .classes(f'size-9 rounded-full flex items-center justify-center transition-colors duration-150 {d.BORDER}'):
        phosphor_icon(icon).classes('opacity-50')
