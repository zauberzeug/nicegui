from pathlib import Path

from ..dependencies import register_library, register_vue_component
from .mixins.content_element import ContentElement

component = register_vue_component(Path('mermaid.js'))
library = register_library(Path('mermaid') / 'mermaid.esm.min.mjs', expose=True)
extras_path = Path(__file__).parent / 'lib' / 'mermaid'
for path in extras_path.glob('*.js'):
    register_library(path.relative_to(extras_path.parent))


class Mermaid(ContentElement):
    CONTENT_PROP = 'content'

    def __init__(self, content: str) -> None:
        '''Mermaid Diagrams

        Renders diagrams and charts written in the Markdown-inspired `Mermaid <https://mermaid.js.org/>`_ language.
        The mermaid syntax can also be used inside Markdown elements by providing the extension string 'mermaid' to the ``ui.markdown`` element.

        :param content: the Mermaid content to be displayed
        '''
        super().__init__(tag='mermaid', content=content)
        self.use_component(component)
        self.use_library(library)

    def on_content_change(self, content: str) -> None:
        self._props[self.CONTENT_PROP] = content.strip()
        self.run_method('update', content.strip())
