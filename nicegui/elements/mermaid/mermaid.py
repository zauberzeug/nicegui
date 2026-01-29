from typing_extensions import Self

from ...defaults import DEFAULT_PROP, resolve_defaults
from ...events import Handler, MermaidNodeClickEventArguments, handle_event
from ..mixins.content_element import ContentElement


class Mermaid(ContentElement, component='mermaid.js', esm={'nicegui-mermaid': 'dist'}):
    CONTENT_PROP = 'content'

    @resolve_defaults
    def __init__(self,
                 content: str,
                 config: dict | None = DEFAULT_PROP | None,
                 *,
                 on_node_click: Handler[MermaidNodeClickEventArguments] | None = None,
                 ) -> None:
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
        :param on_node_click: callback that is invoked when a node is clicked (*added in version 3.3.0*)
        """
        super().__init__(content=content)
        self._props['config'] = config

        if on_node_click is not None:
            self.on_node_click(on_node_click)

    def on_node_click(self, callback: Handler[MermaidNodeClickEventArguments]) -> Self:
        """Add a callback to be invoked when a node is clicked."""
        self.on('node_click', lambda e: handle_event(callback, MermaidNodeClickEventArguments(
            sender=self,
            client=self.client,
            node_id='-'.join(e.args.split('-')[1:-1])  # extract Node ID from HTML ID (<type>-<node_id>-<index>)
        )))
        self._props['clickable'] = True
        return self

    def _handle_content_change(self, content: str) -> None:
        self._props[self.CONTENT_PROP] = content.strip()
        self.run_method('update', content.strip())
