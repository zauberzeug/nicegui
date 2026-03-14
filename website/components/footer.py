from nicegui import ui

GITHUB_SVG = '<svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'
DISCORD_SVG = '<svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor"><path d="M13.55 3.15A13.3 13.3 0 0010.25 2a9.8 9.8 0 00-.43.88 12.3 12.3 0 00-3.64 0A9.8 9.8 0 005.75 2a13.3 13.3 0 00-3.3 1.15A14.2 14.2 0 000 12.05a13.4 13.4 0 004.06 2.06 10 10 0 00.86-1.4 8.7 8.7 0 01-1.36-.65l.33-.26a9.5 9.5 0 008.22 0l.33.26c-.43.25-.89.47-1.36.65.25.5.54.96.86 1.4a13.4 13.4 0 004.06-2.06A14.2 14.2 0 0013.55 3.15zM5.35 10.35c-.87 0-1.57-.8-1.57-1.77s.7-1.77 1.57-1.77 1.58.8 1.57 1.77-.7 1.77-1.57 1.77zm5.3 0c-.87 0-1.57-.8-1.57-1.77s.7-1.77 1.57-1.77 1.58.8 1.57 1.77-.7 1.77-1.57 1.77z"/></svg>'
REDDIT_SVG = '<svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor"><path d="M16 8A8 8 0 110 8a8 8 0 0116 0zm-4.87-2.16a1.07 1.07 0 00-.76.32 5.34 5.34 0 00-2.91-.92l.5-2.33 1.6.34a.76.76 0 10.08-.44l-1.8-.38a.22.22 0 00-.26.17l-.55 2.6a5.38 5.38 0 00-2.98.92 1.07 1.07 0 10-1.18 1.76 2.1 2.1 0 00-.03.36c0 1.82 2.12 3.3 4.74 3.3s4.74-1.48 4.74-3.3a2.1 2.1 0 00-.03-.36 1.07 1.07 0 00-.16-2.04zM5.68 8.84a.76.76 0 111.52 0 .76.76 0 01-1.52 0zm4.26 2.01a2.93 2.93 0 01-1.95.58 2.93 2.93 0 01-1.95-.58.22.22 0 01.31-.31c.43.35 1.04.53 1.64.53s1.21-.18 1.64-.53a.22.22 0 01.31.31zm-.14-1.25a.76.76 0 110-1.52.76.76 0 010 1.52z"/></svg>'


def _footer_column(title: str, links: list[tuple[str, str]]) -> None:
    """Render a footer link column with heading and list of (label, url) pairs."""
    with ui.column().classes('mo-footer-col'):
        ui.label(title).classes('text-xs font-semibold uppercase tracking-wide mb-4') \
            .style('color: var(--mo-text-muted)')
        for label, url in links:
            ui.link(label, url).style('color: var(--mo-text-secondary); font-size: 0.9375rem')


def create() -> None:
    """Create the 4-column footer with brand, links, and bottom bar."""
    with ui.element('footer').classes('mo-footer'):
        with ui.row().classes('mo-footer-inner'):
            # Brand column
            with ui.column().classes('mo-footer-brand'):
                ui.markdown('**Nice**GUI').classes('text-lg')
                ui.label('The Python-based UI framework that shows up in your browser.') \
                    .classes('text-sm').style('color: var(--mo-text-secondary)')
                ui.html(f'''
                    <div class="mo-footer-socials">
                        <a href="https://github.com/zauberzeug/nicegui/" aria-label="GitHub">{GITHUB_SVG}</a>
                        <a href="https://discord.gg/TEpFeAaF4f" aria-label="Discord">{DISCORD_SVG}</a>
                        <a href="https://www.reddit.com/r/nicegui/" aria-label="Reddit">{REDDIT_SVG}</a>
                    </div>
                ''', sanitize=False)

            _footer_column('Resources', [
                ('Documentation', '/documentation'),
                ('Examples', '/examples'),
                ('GitHub', 'https://github.com/zauberzeug/nicegui/'),
                ('PyPI', 'https://pypi.org/project/nicegui/'),
            ])
            _footer_column('Community', [
                ('Discord', 'https://discord.gg/TEpFeAaF4f'),
                ('Contributing', 'https://github.com/zauberzeug/nicegui/blob/main/CONTRIBUTING.md'),
                ('Discussions', 'https://github.com/zauberzeug/nicegui/discussions'),
                ('Sponsors', 'https://github.com/sponsors/zauberzeug'),
            ])
            _footer_column('Legal', [
                ('Imprint', '/imprint_privacy'),
                ('Privacy', '/imprint_privacy'),
            ])

        with ui.row().classes('mo-footer-bottom'):
            ui.markdown('Made with NiceGUI by [Zauberzeug](https://zauberzeug.com)')
            ui.markdown('\u00a9 2025 [Zauberzeug GmbH](https://zauberzeug.com)')
