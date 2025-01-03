from typing import Optional

from typing_extensions import Self

from ..classes import Classes
from ..context import context
from ..element import Element
from ..props import Props
from ..style import Style


class QueryElement(Element, component='query.js'):

    def __init__(self, selector: str) -> None:
        super().__init__()
        self._props['selector'] = selector
        self._props['classes'] = []
        self._props['style'] = {}
        self._props['props'] = {}


class Query:

    def __init__(self, selector: str) -> None:
        """Query Selector

        To manipulate elements like the document body, you can use the `ui.query` function.
        With the query result you can add classes, styles, and attributes like with every other UI element.
        This can be useful for example to change the background color of the page (e.g. `ui.query('body').classes('bg-green')`).

        :param selector: the CSS selector (e.g. "body", "#my-id", ".my-class", "div > p")
        """
        for element in context.client.elements.values():
            if isinstance(element, QueryElement) and element.props['selector'] == selector:
                self.element = element
                break
        else:
            self.element = QueryElement(selector)

    def classes(self,
                add: Optional[str] = None, *,
                remove: Optional[str] = None,
                toggle: Optional[str] = None,
                replace: Optional[str] = None,
                ) -> Self:
        """Apply, remove, toggle, or replace HTML classes.

        This allows modifying the look of the element or its layout using `Tailwind <https://tailwindcss.com/>`_ or `Quasar <https://quasar.dev/>`_ classes.

        Removing or replacing classes can be helpful if predefined classes are not desired.

        :param add: whitespace-delimited string of classes
        :param remove: whitespace-delimited string of classes to remove from the element
        :param toggle: whitespace-delimited string of classes to toggle
        :param replace: whitespace-delimited string of classes to use instead of existing ones
        """
        classes = Classes.update_list(self.element.props['classes'], add, remove, toggle, replace)
        new_classes = [c for c in classes if c not in self.element.props['classes']]
        old_classes = [c for c in self.element.props['classes'] if c not in classes]
        if new_classes:
            self.element.run_method('add_classes', new_classes)
        if old_classes:
            self.element.run_method('remove_classes', old_classes)
        self.element.props['classes'] = classes
        return self

    def style(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) \
            -> Self:
        """Apply, remove, or replace CSS definitions.

        Removing or replacing styles can be helpful if the predefined style is not desired.

        :param add: semicolon-separated list of styles to add to the element
        :param remove: semicolon-separated list of styles to remove from the element
        :param replace: semicolon-separated list of styles to use instead of existing ones
        """
        old_style = Style.parse(remove)
        for key in old_style:
            self.element.props['style'].pop(key, None)
        if old_style:
            self.element.run_method('remove_style', list(old_style))
        self.element.props['style'].update(Style.parse(add))
        self.element.props['style'].update(Style.parse(replace))
        if self.element.props['style']:
            self.element.run_method('add_style', self.element.props['style'])
        return self

    def props(self, add: Optional[str] = None, *, remove: Optional[str] = None) -> Self:
        """Add or remove props.

        This allows modifying the look of the element or its layout using `Quasar <https://quasar.dev/>`_ props.
        Since props are simply applied as HTML attributes, they can be used with any HTML element.

        Boolean properties are assumed ``True`` if no value is specified.

        :param add: whitespace-delimited list of either boolean values or key=value pair to add
        :param remove: whitespace-delimited list of property keys to remove
        """
        old_props = Props.parse(remove)
        for key in old_props:
            self.element.props['props'].pop(key, None)
        if old_props:
            self.element.run_method('remove_props', list(old_props))
        new_props = Props.parse(add)
        self.element.props['props'].update(new_props)
        if self.element.props['props']:
            self.element.run_method('add_props', self.element.props['props'])
        return self
