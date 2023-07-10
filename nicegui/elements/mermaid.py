from pathlib import Path

from .mixins.content_element import ContentElement

base = Path(__file__).parent


class Mermaid(ContentElement,
              component='mermaid.js',
              exposed_libraries=['lib/mermaid/mermaid.esm.min.mjs'],
              extra_libraries=[p.relative_to(base) for p in (base / 'lib' / 'mermaid').glob('*.js')]):
    CONTENT_PROP = 'content'

    def __init__(self, content: str) -> None:
        '''Mermaid Diagrams

        Renders diagrams and charts written in the Markdown-inspired `Mermaid <https://mermaid.js.org/>`_ language.
        The mermaid syntax can also be used inside Markdown elements by providing the extension string 'mermaid' to the ``ui.markdown`` element.

        :param content: the Mermaid content to be displayed
        '''
        super().__init__(content=content)

    def on_content_change(self, content: str) -> None:
        self._props[self.CONTENT_PROP] = content.strip()
        self.run_method('update', content.strip())
