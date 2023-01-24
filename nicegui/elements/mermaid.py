from ..dependencies import register_component
from .mixins.content_element import ContentElement

register_component('mermaid', __file__, 'mermaid.js', ['lib/mermaid.min.js'])


class Mermaid(ContentElement):

    def __init__(self, content: str) -> None:
        super().__init__(tag='mermaid', content=content)

    def on_content_change(self, content: str) -> None:
        self._props['innerHTML'] = content
        self.run_method('update', content)
