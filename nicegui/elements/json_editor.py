from typing import Callable, Dict, Optional

from ..awaitable_response import AwaitableResponse
from ..element import Element
from ..events import GenericEventArguments, JsonEditorChangeEventArguments, JsonEditorSelectEventArguments, handle_event


class JsonEditor(Element, component='json_editor.js', exposed_libraries=['lib/vanilla-jsoneditor/index.js']):

    def __init__(self,
                 properties: Dict, *,
                 on_select: Optional[Callable] = None,
                 on_change: Optional[Callable] = None,
                 ) -> None:
        """JSONEditor

        An element to create a JSON editor using `JSONEditor <https://github.com/josdejong/svelte-jsoneditor>`_.
        Updates can be pushed to the editor by changing the `properties` property.
        After data has changed, call the `update` method to refresh the editor.

        :param properties: dictionary of JSONEditor properties
        :param on_select: callback function that is called when some of the content has been selected
        :param on_change: callback function that is called when the content has changed
        """
        super().__init__()
        self._props['properties'] = properties

        if on_select:
            def handle_on_select(e: GenericEventArguments) -> None:
                handle_event(on_select, JsonEditorSelectEventArguments(sender=self, client=self.client, **e.args))
            self.on('select', handle_on_select, ['selection'])

        if on_change:
            def handle_on_change(e: GenericEventArguments) -> None:
                handle_event(on_change, JsonEditorChangeEventArguments(sender=self, client=self.client, **e.args))
            self.on('change', handle_on_change, ['content', 'errors'])

    @property
    def properties(self) -> Dict:
        """The property dictionary."""
        return self._props['properties']

    def update(self) -> None:
        super().update()
        self.run_method('update_editor')

    def run_editor_method(self, name: str, *args, timeout: float = 1,
                          check_interval: float = 0.01) -> AwaitableResponse:
        """Run a method of the JSONEditor instance.

        See the `JSONEditor README <https://github.com/josdejong/svelte-jsoneditor/>`_ for a list of methods.

        If the function is awaited, the result of the method call is returned.
        Otherwise, the method is executed without waiting for a response.

        :param name: name of the method (a prefix ":" indicates that the arguments are JavaScript expressions)
        :param args: arguments to pass to the method (Python objects or JavaScript expressions)
        :param timeout: timeout in seconds (default: 1 second)
        :param check_interval: interval in seconds to check for a response (default: 0.01 seconds)

        :return: AwaitableResponse that can be awaited to get the result of the method call
        """
        return self.run_method('run_editor_method', name, *args, timeout=timeout, check_interval=check_interval)
