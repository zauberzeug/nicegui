from typing import Dict, Optional

from typing_extensions import Self

from ..awaitable_response import AwaitableResponse
from ..element import Element
from ..events import (
    GenericEventArguments,
    Handler,
    JsonEditorChangeEventArguments,
    JsonEditorSelectEventArguments,
    handle_event,
)


class JsonEditor(Element, component='json_editor.js', dependencies=['lib/vanilla-jsoneditor/standalone.js']):

    def __init__(self,
                 properties: Dict, *,
                 on_select: Optional[Handler[JsonEditorSelectEventArguments]] = None,
                 on_change: Optional[Handler[JsonEditorChangeEventArguments]] = None,
                 schema: Optional[Dict] = None,
                 ) -> None:
        """JSONEditor

        An element to create a JSON editor using `JSONEditor <https://github.com/josdejong/svelte-jsoneditor>`_.
        Updates can be pushed to the editor by changing the `properties` property.
        After data has changed, call the `update` method to refresh the editor.

        :param properties: dictionary of JSONEditor properties
        :param on_select: callback which is invoked when some of the content has been selected
        :param on_change: callback which is invoked when the content has changed
        :param schema: optional `JSON schema <https://json-schema.org/>`_ for validating the data being edited
        """
        super().__init__()
        self._props['properties'] = properties

        if schema:
            self._props['schema'] = schema

        if on_select:
            self.on_select(on_select)

        if on_change:
            self.on_change(on_change)

    def on_change(self, callback: Handler[JsonEditorChangeEventArguments]) -> Self:
        """Add a callback to be invoked when the content changes."""
        def handle_on_change(e: GenericEventArguments) -> None:
            handle_event(callback, JsonEditorChangeEventArguments(sender=self, client=self.client, **e.args))
        self.on('change', handle_on_change, ['content', 'errors'])
        return self

    def on_select(self, callback: Handler[JsonEditorSelectEventArguments]) -> Self:
        """Add a callback to be invoked when some of the content has been selected."""
        def handle_on_select(e: GenericEventArguments) -> None:
            handle_event(callback, JsonEditorSelectEventArguments(sender=self, client=self.client, **e.args))
        self.on('select', handle_on_select, ['selection'])
        return self

    @property
    def properties(self) -> Dict:
        """The property dictionary."""
        return self._props['properties']

    def update(self) -> None:
        super().update()
        self.run_method('update_editor')

    def run_editor_method(self, name: str, *args, timeout: float = 1) -> AwaitableResponse:
        """Run a method of the JSONEditor instance.

        See the `JSONEditor README <https://github.com/josdejong/svelte-jsoneditor/>`_ for a list of methods.

        If the function is awaited, the result of the method call is returned.
        Otherwise, the method is executed without waiting for a response.

        :param name: name of the method (a prefix ":" indicates that the arguments are JavaScript expressions)
        :param args: arguments to pass to the method (Python objects or JavaScript expressions)
        :param timeout: timeout in seconds (default: 1 second)

        :return: AwaitableResponse that can be awaited to get the result of the method call
        """
        return self.run_method('run_editor_method', name, *args, timeout=timeout)
