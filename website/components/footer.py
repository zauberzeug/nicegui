from nicegui import ui

_GITHUB_ICON = '<svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'
_DISCORD_ICON = '<svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor"><path d="M13.55 3.15A13.3 13.3 0 0010.25 2a9.8 9.8 0 00-.43.88 12.3 12.3 0 00-3.64 0A9.8 9.8 0 005.75 2a13.3 13.3 0 00-3.3 1.15A14.2 14.2 0 000 12.05a13.4 13.4 0 004.06 2.06 10 10 0 00.86-1.4 8.7 8.7 0 01-1.36-.65l.33-.26a9.5 9.5 0 008.22 0l.33.26c-.43.25-.89.47-1.36.65.25.5.54.96.86 1.4a13.4 13.4 0 004.06-2.06A14.2 14.2 0 0013.55 3.15zM5.35 10.35c-.87 0-1.57-.8-1.57-1.77s.7-1.77 1.57-1.77 1.58.8 1.57 1.77-.7 1.77-1.57 1.77zm5.3 0c-.87 0-1.57-.8-1.57-1.77s.7-1.77 1.57-1.77 1.58.8 1.57 1.77-.7 1.77-1.57 1.77z"/></svg>'
_REDDIT_ICON = '<svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor"><path d="M16 8A8 8 0 110 8a8 8 0 0116 0zm-4.87-2.16a1.07 1.07 0 00-.76.32 5.34 5.34 0 00-2.91-.92l.5-2.33 1.6.34a.76.76 0 10.08-.44l-1.8-.38a.22.22 0 00-.26.17l-.55 2.6a5.38 5.38 0 00-2.98.92 1.07 1.07 0 10-1.18 1.76 2.1 2.1 0 00-.03.36c0 1.82 2.12 3.3 4.74 3.3s4.74-1.48 4.74-3.3a2.1 2.1 0 00-.03-.36 1.07 1.07 0 00-.16-2.04zM5.68 8.84a.76.76 0 111.52 0 .76.76 0 01-1.52 0zm4.26 2.01a2.93 2.93 0 01-1.95.58 2.93 2.93 0 01-1.95-.58.22.22 0 01.31-.31c.43.35 1.04.53 1.64.53s1.21-.18 1.64-.53a.22.22 0 01.31.31zm-.14-1.25a.76.76 0 110-1.52.76.76 0 010 1.52z"/></svg>'


def create() -> None:
    """Create the 4-column footer with brand, links, and bottom bar."""
    with ui.element('footer').classes('mo-footer'):
        with ui.element('div').classes('mo-footer-inner'):
            # Brand column
            with ui.element('div').classes('mo-footer-brand'):
                ui.html('<div class="mo-footer-brand-logo"><strong>Nice</strong>GUI</div>', sanitize=False)
                ui.html(
                    '<p class="mo-footer-tagline">'
                    'The Python-based UI framework that shows up in your browser.'
                    '</p>',
                    sanitize=False,
                )
                ui.html(f'''
                    <div class="mo-footer-socials">
                        <a href="https://github.com/zauberzeug/nicegui/" aria-label="GitHub">{_GITHUB_ICON}</a>
                        <a href="https://discord.gg/TEpFeAaF4f" aria-label="Discord">{_DISCORD_ICON}</a>
                        <a href="https://www.reddit.com/r/nicegui/" aria-label="Reddit">{_REDDIT_ICON}</a>
                    </div>
                ''', sanitize=False)

            # Resources column
            with ui.element('div').classes('mo-footer-col'):
                ui.html('<h4>Resources</h4>', sanitize=False)
                ui.html('''<ul>
                    <li><a href="/documentation">Documentation</a></li>
                    <li><a href="/examples">Examples</a></li>
                    <li><a href="https://github.com/zauberzeug/nicegui/">GitHub</a></li>
                    <li><a href="https://pypi.org/project/nicegui/">PyPI</a></li>
                </ul>''', sanitize=False)

            # Community column
            with ui.element('div').classes('mo-footer-col'):
                ui.html('<h4>Community</h4>', sanitize=False)
                ui.html('''<ul>
                    <li><a href="https://discord.gg/TEpFeAaF4f">Discord</a></li>
                    <li><a href="https://github.com/zauberzeug/nicegui/blob/main/CONTRIBUTING.md">Contributing</a></li>
                    <li><a href="https://github.com/zauberzeug/nicegui/discussions">Discussions</a></li>
                    <li><a href="https://github.com/sponsors/zauberzeug">Sponsors</a></li>
                </ul>''', sanitize=False)

            # Legal column
            with ui.element('div').classes('mo-footer-col'):
                ui.html('<h4>Legal</h4>', sanitize=False)
                ui.html('''<ul>
                    <li><a href="/imprint_privacy">Imprint</a></li>
                    <li><a href="/imprint_privacy">Privacy</a></li>
                </ul>''', sanitize=False)

        with ui.element('div').classes('mo-footer-bottom'):
            ui.html(
                '<span>Made with NiceGUI by <a href="https://zauberzeug.com">Zauberzeug</a></span>',
                sanitize=False,
            )
            ui.html(
                '<span>&copy; 2025 <a href="https://zauberzeug.com">Zauberzeug GmbH</a></span>',
                sanitize=False,
            )
