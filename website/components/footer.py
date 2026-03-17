from nicegui import ui


def create() -> None:
    """Create the 4-column footer with brand, links, and bottom bar."""
    with ui.element('footer').classes('mo-footer w-full pt-20 px-6').style('border-top: 1px solid var(--mo-border)'):
        with ui.grid().classes('max-w-[1280px] mx-auto w-full pb-12 gap-12 '
                               'grid-cols-[2fr_1fr_1fr_1fr] max-sm:grid-cols-1'):
            with ui.column().classes('gap-3'):
                ui.markdown('**Nice**GUI').classes('text-lg -mt-3')
                ui.label('The Python-based UI framework that shows up in your browser.') \
                    .classes('text-sm leading-normal text-(--mo-text-secondary)')
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

        with ui.row().classes('max-w-[1280px] mx-auto w-full py-5 justify-between items-center text-[0.8125rem] text-(--mo-text-muted)') \
                .style('border-top: 1px solid var(--mo-border)'):
            ui.markdown('Made with NiceGUI by [Zauberzeug](https://zauberzeug.com)')
            ui.markdown('\u00a9 2025 [Zauberzeug GmbH](https://zauberzeug.com)')


def _column(title: str, links: list[tuple[str, str]]) -> None:
    """Render a footer link column with heading and list of (label, url) pairs."""
    with ui.column().classes('gap-2.5'):
        ui.label(title).classes('text-xs font-semibold uppercase tracking-widest mb-4 text-(--mo-text-muted)')
        for label, url in links:
            ui.link(label, url).classes(
                'text-[0.9375rem] no-underline transition-colors duration-150 text-(--mo-text-secondary)')


def _icon_link(icon: str, url: str) -> None:
    """Render a circular icon link with hover effect."""
    with ui.link(target=url).classes(
        'size-9 rounded-full flex items-center justify-center pt-1 transition-colors duration-150'
    ).style('border: 1px solid var(--mo-border)'):
        ui.html(f'<i class="ph-duotone {icon}"></i>', sanitize=False).classes('opacity-50')
