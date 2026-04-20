import weakref

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
                self._element = weakref.ref(element)
                break
        else:
            self._element = weakref.ref(QueryElement(selector))

    @property
    def element(self) -> QueryElement:
        """The element this query belongs to."""
        element = self._element()
        if element is None:
            raise RuntimeError('The element this query belongs to has been deleted.')
        return element

    def classes(self,
                add: str | None = None, *,
                remove: str | None = None,
                toggle: str | None = None,
                replace: str | None = None,
                ) -> Self:
        """Apply, remove, toggle, or replace HTML classes.

        This allows modifying the look of the element or its layout using `Tailwind <https://tailwindcss.com/>`_ or `Quasar <https://quasar.dev/>`_ classes.

        Removing or replacing classes can be helpful if predefined classes are not desired.

        :param add: whitespace-delimited string of classes
        :param remove: whitespace-delimited string of classes to remove from the element
        :param toggle: whitespace-delimited string of classes to toggle (*added in version 2.7.0*)
        :param replace: whitespace-delimited string of classes to use instead of existing ones
        """
        element = self.element
        classes = Classes.update_list(element.props['classes'], add, remove, toggle, replace)
        new_classes = [c for c in classes if c not in element.props['classes']]
        old_classes = [c for c in element.props['classes'] if c not in classes]
        if new_classes:
            element.run_method('add_classes', new_classes)
        if old_classes:
            element.run_method('remove_classes', old_classes)
        element.props['classes'] = classes
        return self

    def style(self, add: str | None = None, *, remove: str | None = None, replace: str | None = None) \
            -> Self:
        """Apply, remove, or replace CSS definitions.

        Removing or replacing styles can be helpful if the predefined style is not desired.

        :param add: semicolon-separated list of styles to add to the element
        :param remove: semicolon-separated list of styles to remove from the element
        :param replace: semicolon-separated list of styles to use instead of existing ones
        """
        element = self.element
        old_style = Style.parse(remove)
        for key in old_style:
            element.props['style'].pop(key, None)
        if old_style:
            element.run_method('remove_style', list(old_style))
        element.props['style'].update(Style.parse(add))
        element.props['style'].update(Style.parse(replace))
        if element.props['style']:
            element.run_method('add_style', element.props['style'])
        return self

    def props(self, add: str | None = None, *, remove: str | None = None) -> Self:
        """Add or remove props.

        This allows modifying the look of the element or its layout using `Quasar <https://quasar.dev/>`_ props.
        Since props are simply applied as HTML attributes, they can be used with any HTML element.

        Boolean properties are assumed ``True`` if no value is specified.

        :param add: whitespace-delimited list of either boolean values or key=value pair to add
        :param remove: whitespace-delimited list of property keys to remove
        """
        element = self.element
        old_props = Props.parse(remove)
        for key in old_props:
            element.props['props'].pop(key, None)
        if old_props:
            element.run_method('remove_props', list(old_props))
        new_props = Props.parse(add)
        element.props['props'].update(new_props)
        if element.props['props']:
            element.run_method('add_props', element.props['props'])
        return self
