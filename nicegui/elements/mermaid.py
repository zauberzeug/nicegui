import uuid
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

    def __init__(self, content: str, config: Optional[Dict] = None, *,
                 on_node_click: Optional[Handler[GenericEventArguments]] = None,
                 function_placeholder: str = 'NICEGUI_HANDLER') -> None:
        """Mermaid Diagrams

        Renders diagrams and charts written in the Markdown-inspired `Mermaid <https://mermaid.js.org/>`_ language.
        The mermaid syntax can also be used inside Markdown elements by providing the extension string 'mermaid' to the ``ui.markdown`` element.

        The optional configuration dictionary is passed directly to mermaid before the first diagram is rendered.
        This can be used to set such options as

            ``{'securityLevel': 'loose', ...}`` - allow running JavaScript when a node is clicked
            ``{'logLevel': 'info', ...}`` - log debug info to the console

        Refer to the Mermaid documentation for the ``mermaid.initialize()`` method for a full list of options.

        :param content: the Mermaid content to be displayed. If ``on_node_click`` is passed, expect lines such as ``click A NICEGUI_HANDLER()``, where ``NICEGUI_HANDLER`` is a placeholder for the JavaScript function defined by NiceGUI to handle node clicks.
        :param config: configuration dictionary to be passed to ``mermaid.initialize()``
        :param on_node_click: a callback function that will be called when a node is clicked. The function should accept an event argument
        :param function_placeholder: the placeholder string to be used in the content for the click handler function. Defaults to "NICEGUI_HANDLER". Customizing it allows you to avoid conflicts with your Mermaid diagram content.
        """
        super().__init__(content=content)
        self._props['config'] = config if config is not None else {}

        if on_node_click is not None:
            self.on('nodeClicked', on_node_click)
            self._props['config']['securityLevel'] = 'loose'
            self._props['function_name'] = f'mermaid_click_handler_{uuid.uuid4().hex}' if on_node_click else None
            self._props['function_placeholder'] = function_placeholder

    def _handle_content_change(self, content: str) -> None:
        self._props[self.CONTENT_PROP] = content.strip()
        self.run_method('update', content.strip())
