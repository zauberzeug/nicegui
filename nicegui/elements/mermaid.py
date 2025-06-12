import uuid
from typing import Dict, Optional

from ..events import GenericEventArguments, Handler
from ..logging import log
from .mixins.content_element import ContentElement


class Mermaid(ContentElement,
              component='mermaid.js',
              dependencies=[
                  'lib/mermaid/mermaid.esm.min.mjs',
                  'lib/mermaid/chunks/mermaid.esm.min/*.mjs',
              ]):
    CONTENT_PROP = 'content'

    def __init__(self, content: str, config: Optional[Dict] = None, *, on_node_click: Optional[Handler[GenericEventArguments]] = None) -> None:
        """Mermaid Diagrams

        Renders diagrams and charts written in the Markdown-inspired `Mermaid <https://mermaid.js.org/>`_ language.
        The mermaid syntax can also be used inside Markdown elements by providing the extension string 'mermaid' to the ``ui.markdown`` element.

        The optional configuration dictionary is passed directly to mermaid before the first diagram is rendered.
        This can be used to set such options as

            ``{'securityLevel': 'loose', ...}`` - allow running JavaScript when a node is clicked
            ``{'logLevel': 'info', ...}`` - log debug info to the console

        Refer to the Mermaid documentation for the ``mermaid.initialize()`` method for a full list of options.

        :param content: the Mermaid content to be displayed. If ``on_node_click`` is passed, expect lines such as ``click A {handler}()``, where ``{handler}`` is a placeholder for the JavaScript function defined by NiceGUI to handle node clicks.
        :param config: configuration dictionary to be passed to ``mermaid.initialize()``
        :param on_node_click: a callback function that will be called when a node is clicked. The function should accept an event argument
        """
        function_name = f'mermaid_click_handler_{uuid.uuid4().hex}' if on_node_click else None
        super().__init__(content=self._format_content(content, function_name))
        self._props['config'] = config if config is not None else {}

        if on_node_click is not None:
            self.on('nodeClicked', on_node_click)
            self._props['config']['securityLevel'] = 'loose'
            self._props['function_name'] = function_name

    def _handle_content_change(self, content: str) -> None:
        content_final = self._format_content(content, self._props.get('function_name'))
        self._props[self.CONTENT_PROP] = content_final
        self.run_method('update', content_final)

    @staticmethod
    def _format_content(content: str, function_name: Optional[str]) -> str:
        content_final = content.strip()
        if function_name is not None:
            try:
                content_final = content_final.format(handler=function_name)
            except KeyError:
                log.warning(
                    'Mermaid content does not contain {handler} placeholder, but node click functionality is enabled. Please add {handler} to the content string.')
        return content_final
