from typing import Callable, Dict, List, Optional

from ..element import Element
from ..events import (GenericEventArguments, JSONEditorOnChangeEventArguments, JSONEditorOnSelectJSONEventArguments,
                      JSONEditorOnSelectTextEventArguments, handle_event)


class JSONEditor(Element, component='jsoneditor.js', exposed_libraries=['lib/vanilla-jsoneditor/index.js']):
    def __init__(
            self, properties: Dict, on_select: Optional[Callable] = None, on_change: Optional[Callable] = None) -> None:
        """JSONEditor

        An element to create a JSON editor using `JSONEditor <https://github.com/josdejong/svelte-jsoneditor>`_.
        Updates can be pushed to the editor by changing the `properties` property.
        After data has changed, call the `update` method to refresh the editor.

        :param properties: dictionary of JSONEditor properties
        :param on_select: callback function that is called when the editor's content has been selected
        :param on_change: callback function that is called when the editor's content has changed
        """
        super().__init__()
        self._props['properties'] = properties
        self._classes = ['nicegui-jsoneditor']

        if on_select:
            def handle_on_select_json(e: GenericEventArguments) -> None:
                handle_event(on_select, JSONEditorOnSelectJSONEventArguments(
                    sender=self,
                    client=self.client,
                    event_type='select',
                    edit=e.args['edit'],
                    path=e.args['path'],
                    type=e.args['type']
                ))
            self.on('select_json', handle_on_select_json, ['edit', 'path', 'type'])

            def handle_on_select_text(e: GenericEventArguments) -> None:
                handle_event(on_select, JSONEditorOnSelectTextEventArguments(
                    sender=self,
                    client=self.client,
                    event_type='select',
                    main=e.args['main'],
                    ranges=e.args['ranges'],
                    type=e.args['type']
                ))
            self.on('select_text', handle_on_select_text, ['main', 'ranges', 'type'])
        if on_change:
            def handle_on_change(e: GenericEventArguments) -> None:
                handle_event(on_change, JSONEditorOnChangeEventArguments(
                    sender=self,
                    client=self.client,
                    event_type='change',
                    content=e.args['content'],
                    errors=e.args['errors']
                ))
            self.on('change', handle_on_change, ['content', 'errors'])

    @property
    def properties(self) -> Dict:
        return self._props['properties']

    def update(self) -> None:
        super().update()
        self.run_method('update_editor')
