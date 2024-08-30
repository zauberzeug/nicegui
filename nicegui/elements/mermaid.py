from typing import Dict, Optional

from .mixins.content_element import ContentElement


class Mermaid(ContentElement,
              component='mermaid.js',
              dependencies=[
                  'lib/mermaid/*.js',
                  'lib/mermaid/mermaid.esm.min.mjs',
                  'lib/mermaid/chunks/mermaid.esm.min/*.mjs',
              ]):
    CONTENT_PROP = 'content'

    def __init__(self, content: str, config: Optional[Dict] = None) -> None:
        """Mermaid Diagrams

        Renders diagrams and charts written in the Markdown-inspired `Mermaid <https://mermaid.js.org/>`_ language.
        The mermaid syntax can also be used inside Markdown elements by providing the extension string 'mermaid' to the ``ui.markdown`` element.

        The optional configuration dictionary is passed directly to mermaid before the first diagram is rendered.
        This can be used to set such options as

            ``{'securityLevel': 'loose', ...}`` - allow running JavaScript when a node is clicked
            ``{'logLevel': 'info', ...}`` - log debug info to the console

        Refer to the Mermaid documentation for the ``mermaid.initialize()`` method for a full list of options.

        :param content: the Mermaid content to be displayed
        :param config: configuration dictionary to be passed to ``mermaid.initialize()``
        """
        super().__init__(content=content)
        self._props['config'] = config

    def _handle_content_change(self, content: str) -> None:
        self._props[self.CONTENT_PROP] = content.strip()
        self.run_method('update', content.strip())
