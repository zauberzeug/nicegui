from .mixins.content_element import ContentElement


class Mermaid(ContentElement,
              component='mermaid.js',
              exposed_libraries=['lib/mermaid/mermaid.esm.min.mjs'],
              extra_libraries=['lib/mermaid/*.js']):
    CONTENT_PROP = 'content'

    def __init__(self, content: str) -> None:
        """Mermaid Diagrams

        Renders diagrams and charts written in the Markdown-inspired `Mermaid <https://mermaid.js.org/>`_ language.
        The mermaid syntax can also be used inside Markdown elements by providing the extension string 'mermaid' to the ``ui.markdown`` element.

        :param content: the Mermaid content to be displayed
        """
        super().__init__(content=content)

    def _handle_content_change(self, content: str) -> None:
        self._props[self.CONTENT_PROP] = content.strip()
        self.run_method('update', content.strip())
