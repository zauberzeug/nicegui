from typing import Any, Callable, Optional

from ..element import Element
from ..events import ClickEventArguments, handle_event
from .mixins.disableable_element import DisableableElement
from .mixins.text_element import TextElement


class List(Element):

    def __init__(self) -> None:
        """List

        A list element based on Quasar's `QList <https://quasar.dev/vue-components/list-and-list-items#qlist-api>`_ component.
        It provides a container for list items.
        """
        super().__init__('q-list')


class Item(DisableableElement):

    def __init__(self, *, on_click: Optional[Callable[..., Any]] = None) -> None:
        """List Item

        Creates a list item based on Quasar's `QItem <https://quasar.dev/vue-components/list-and-list-items#qitem-api>`_ component.
        The item should be placed inside a list element.
        """
        super().__init__(tag='q-item')

        if on_click:
            self._props['clickable'] = True
            self.on('click', lambda _: handle_event(on_click, ClickEventArguments(sender=self, client=self.client)))


class ItemSection(Element):

    def __init__(self) -> None:
        """
        List Item Section

        Creates an item section based on Quasar's `QItemList <https://quasar.dev/vue-components/list-and-list-items#qitemsection-api>`_ component.
        The section should be placed inside a list item element.
        """
        super().__init__('q-item-section')


class ItemLabel(TextElement):

    def __init__(self, text: str = '') -> None:
        """
        List Item Label

        Creates an item label based on Quasar's `QItemLabel <https://quasar.dev/vue-components/list-and-list-items#qitemlabel-api>`_ component.

        :param text: text to be displayed (default: "")
        """
        super().__init__(tag='q-item-label', text=text)
