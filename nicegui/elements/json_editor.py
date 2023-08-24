from typing import Callable, Dict, Optional

from ..element import Element
from ..events import (GenericEventArguments, JsonEditorChangeEventArguments, JsonEditorSelectJsonEventArguments,
                      JsonEditorSelectTextEventArguments, handle_event)


class JsonEditor(Element, component='json_editor.js', exposed_libraries=['lib/vanilla-jsoneditor/index.js']):

    def __init__(self,
                 properties: Dict, *,
                 on_select_json: Optional[Callable] = None,
                 on_select_text: Optional[Callable] = None,
                 on_change: Optional[Callable] = None,
                 ) -> None:
        """JSONEditor

        An element to create a JSON editor using `JSONEditor <https://github.com/josdejong/svelte-jsoneditor>`_.
        Updates can be pushed to the editor by changing the `properties` property.
        After data has changed, call the `update` method to refresh the editor.

        :param properties: dictionary of JSONEditor properties
        :param on_select_json: callback function that is called when a JSON path is selected
        :param on_select_text: callback function that is called when text is selected
        :param on_change: callback function that is called when the editor's content has changed
        """
        super().__init__()
        self._props['properties'] = properties
        self._classes = ['nicegui-json-editor']

        if on_select_json:
            def handle_select_json(e: GenericEventArguments) -> None:
                handle_event(on_select_json,
                             JsonEditorSelectJsonEventArguments(sender=self, client=self.client, **e.args))
            self.on('select_json', handle_select_json, ['edit', 'path', 'type'])

        if on_select_text:
            def handle_on_select_text(e: GenericEventArguments) -> None:
                handle_event(on_select_text,
                             JsonEditorSelectTextEventArguments(sender=self, client=self.client, **e.args))
            self.on('select_text', handle_on_select_text, ['main', 'ranges', 'type'])

        if on_change:
            def handle_on_change(e: GenericEventArguments) -> None:
                handle_event(on_change,
                             JsonEditorChangeEventArguments(sender=self, client=self.client, **e.args))
            self.on('change', handle_on_change, ['content', 'errors'])

    @property
    def properties(self) -> Dict:
        return self._props['properties']

    def update(self) -> None:
        super().update()
        self.run_method('update_editor')
