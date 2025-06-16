from typing import Dict, Optional

from ..events import GenericEventArguments, Handler
from .mixins.content_element import ContentElement


class Mermaid(ContentElement,
              component='mermaid.js',
              dependencies=[
                  'lib/mermaid/mermaid.esm.min.mjs',
                  'lib/mermaid/chunks/mermaid.esm.min/*.mjs',
              ]):
    CONTENT_PROP = 'content'

    def __init__(self, content: str, config: Optional[Dict] = None, on_node_click: Optional[Handler[GenericEventArguments]] = None) -> None:
        """Mermaid Diagrams

            Renders diagrams and charts written in the Markdown-inspired `Mermaid <https://mermaid.js.org/>`_ language.
            The mermaid syntax can also be used inside Markdown elements by providing the extension string 'mermaid' to the ``ui.markdown`` element.

            The optional configuration dictionary is passed directly to mermaid before the first diagram is rendered.
            This can be used to set such options as

                ``{'securityLevel': 'loose', ...}`` - allow running JavaScript when a node is clicked, applied automatically when `on_node_clicked` is specified
                ``{'logLevel': 'info', ...}`` - log debug info to the console

            Refer to the Mermaid documentation for the ``mermaid.initialize()`` method for a full list of options.

            :param content: the Mermaid content to be displayed
            :param config: configuration dictionary to be passed to ``mermaid.initialize()``
            :param on_node_click: callback that is invoked when a node is clicked, applies ``{'securityLevel': 'loose'}`` automatically
            """

        super().__init__(content=content)

        self._props['config'] = config or {}

        if on_node_click:
            self.on('nodeClick', on_node_click)
            self._props['config']['securityLevel'] = 'loose'
            self._props['clickInstance'] = True

    def _handle_content_change(self, content: str) -> None:
        self._props[self.CONTENT_PROP] = content.strip()
        self.run_method('update', content.strip())
