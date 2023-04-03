from typing import Optional

from typing_extensions import Self

from ..dependencies import register_component
from ..element import Element
from ..globals import get_client

register_component('query', __file__, 'query.js')


class Query(Element):

    def __init__(self, selector: str) -> None:
        super().__init__('query')
        self._props['selector'] = selector
        self._props['classes'] = []
        self._props['style'] = {}
        self._props['props'] = {}

    def classes(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) \
            -> Self:
        classes = self._update_classes_list(self._props['classes'], add, remove, replace)
        new_classes = [c for c in classes if c not in self._props['classes']]
        old_classes = [c for c in self._props['classes'] if c not in classes]
        if new_classes:
            self.run_method('add_classes', new_classes)
        if old_classes:
            self.run_method('remove_classes', old_classes)
        self._props['classes'] = classes
        return self

    def style(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) \
            -> Self:
        old_style = Element._parse_style(remove)
        for key in old_style:
            self._props['style'].pop(key, None)
        if old_style:
            self.run_method('remove_style', list(old_style))
        self._props['style'].update(Element._parse_style(add))
        self._props['style'].update(Element._parse_style(replace))
        if self._props['style']:
            self.run_method('add_style', self._props['style'])
        return self

    def props(self, add: Optional[str] = None, *, remove: Optional[str] = None) -> Self:
        old_props = self._parse_props(remove)
        for key in old_props:
            self._props['props'].pop(key, None)
        if old_props:
            self.run_method('remove_props', list(old_props))
        new_props = self._parse_props(add)
        self._props['props'].update(new_props)
        if self._props['props']:
            self.run_method('add_props', self._props['props'])
        return self


def query(selector: str) -> Query:
    """Query Selector

    To manipulate elements like the document body, you can use the `ui.query` function.
    With the query result you can add classes, styles, and attributes like with every other UI element.
    This can be useful for example to change the background color of the page (e.g. `ui.query('body').classes('bg-green')`).
    """
    for element in get_client().elements.values():
        if isinstance(element, Query) and element._props['selector'] == selector:
            return element
    return Query(selector)
