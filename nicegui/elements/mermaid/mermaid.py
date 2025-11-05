from typing import Optional

from ...events import GenericEventArguments, Handler
from ..mixins.content_element import ContentElement


class Mermaid(ContentElement, component='mermaid.js', esm={'nicegui-mermaid': 'dist'}):
    CONTENT_PROP = 'content'

    def __init__(self, content: str, config: Optional[dict] = None, *, on_node_click: Optional[Handler[GenericEventArguments]] = None) -> None:
        """Mermaid Diagrams

        Renders diagrams and charts written in the Markdown-inspired `Mermaid <https://mermaid.js.org/>`_ language.
        The mermaid syntax can also be used inside Markdown elements by providing the extension string 'mermaid' to the ``ui.markdown`` element.

        The optional configuration dictionary is passed directly to mermaid before the first diagram is rendered.
        This can be used to set such options as

            ``{'securityLevel': 'loose', ...}`` - allow running JavaScript when a node is clicked
            ``{'logLevel': 'info', ...}`` - log debug info to the console

        Refer to the Mermaid documentation for the ``mermaid.initialize()`` method for a full list of options.

        **Note:** When using click handlers with ``securityLevel: 'loose'``,
        make sure to use unique node IDs across diagrams to avoid click events being bound to the wrong elements.

        :param content: the Mermaid content to be displayed
        :param config: configuration dictionary to be passed to ``mermaid.initialize()``
        :param on_node_click: callback that is invoked when a node is clicked
        """
        super().__init__(content=content)
        self._props['config'] = config

        if on_node_click is not None:
            self.on('node_click', on_node_click)
            self._props['clickInstance'] = True

    def _handle_content_change(self, content: str) -> None:
        self._props[self.CONTENT_PROP] = content.strip()
        self.run_method('update', content.strip())
