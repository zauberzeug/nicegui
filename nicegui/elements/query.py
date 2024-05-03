from typing import Optional

from typing_extensions import Self

from ..context import context
from ..element import Element


class QueryElement(Element, component='query.js'):

    def __init__(self, selector: str) -> None:
        super().__init__()
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


class Query:

    def __init__(self, selector: str) -> None:
        """Query Selector

        To manipulate elements like the document body, you can use the `ui.query` function.
        With the query result you can add classes, styles, and attributes like with every other UI element.
        This can be useful for example to change the background color of the page (e.g. `ui.query('body').classes('bg-green')`).

        :param selector: the CSS selector (e.g. "body", "#my-id", ".my-class", "div > p")
        """
        for element in context.client.elements.values():
            if isinstance(element, QueryElement) and element._props['selector'] == selector:  # pylint: disable=protected-access
                self.element = element
                break
        else:
            self.element = QueryElement(selector)

    def classes(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) \
            -> Self:
        """Apply, remove, or replace HTML classes.

        This allows modifying the look of the element or its layout using `Tailwind <https://tailwindcss.com/>`_ or `Quasar <https://quasar.dev/>`_ classes.

        Removing or replacing classes can be helpful if predefined classes are not desired.

        :param add: whitespace-delimited string of classes
        :param remove: whitespace-delimited string of classes to remove from the element
        :param replace: whitespace-delimited string of classes to use instead of existing ones
        """
        self.element.classes(add, remove=remove, replace=replace)
        return self

    def style(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) \
            -> Self:
        """Apply, remove, or replace CSS definitions.

        Removing or replacing styles can be helpful if the predefined style is not desired.

        :param add: semicolon-separated list of styles to add to the element
        :param remove: semicolon-separated list of styles to remove from the element
        :param replace: semicolon-separated list of styles to use instead of existing ones
        """
        self.element.style(add, remove=remove, replace=replace)
        return self

    def props(self, add: Optional[str] = None, *, remove: Optional[str] = None) -> Self:
        """Add or remove props.

        This allows modifying the look of the element or its layout using `Quasar <https://quasar.dev/>`_ props.
        Since props are simply applied as HTML attributes, they can be used with any HTML element.

        Boolean properties are assumed ``True`` if no value is specified.

        :param add: whitespace-delimited list of either boolean values or key=value pair to add
        :param remove: whitespace-delimited list of property keys to remove
        """
        self.element.props(add, remove=remove)
        return self
