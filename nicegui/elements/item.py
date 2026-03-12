from typing_extensions import Self

from ..events import ClickEventArguments, Handler, handle_event
from .mixins.disableable_element import DisableableElement
from .mixins.text_element import TextElement


class Item(DisableableElement):

    def __init__(self, text: str = '', *, on_click: Handler[ClickEventArguments] | None = None) -> None:
        """List Item

        Creates a clickable list item based on Quasar's
        `QItem <https://quasar.dev/vue-components/list-and-list-items#qitem-api>`_ component.
        The item should be placed inside a ``ui.list`` or ``ui.menu`` element.
        If the text parameter is provided, an item section will be created with the given text.
        If you want to customize how the text is displayed, you need to create your own item section and label elements.

        :param text: text to be displayed (default: "")
        :param on_click: callback to be executed when clicking on the item (sets the "clickable" prop to True)
        """
        super().__init__(tag='q-item')

        if on_click:
            self.on_click(on_click)

        if text:
            with self:
                ItemSection(text=text)

    def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
        """Add a callback to be invoked when the List Item is clicked."""
        self._props['clickable'] = True  # idempotent
        self.on('click', lambda _: handle_event(callback, ClickEventArguments(sender=self, client=self.client)))
        return self


class ItemSection(TextElement):

    def __init__(self, text: str = '') -> None:
        """List Item Section

        Creates an item section based on Quasar's
        `QItemSection <https://quasar.dev/vue-components/list-and-list-items#qitemsection-api>`_ component.
        The section should be placed inside a ``ui.item`` element.

        :param text: text to be displayed (default: "")
        """
        super().__init__(tag='q-item-section', text=text)


class ItemLabel(TextElement):

    def __init__(self, text: str = '') -> None:
        """List Item Label

        Creates an item label based on Quasar's `QItemLabel <https://quasar.dev/vue-components/list-and-list-items#qitemlabel-api>`_ component.

        :param text: text to be displayed (default: "")
        """
        super().__init__(tag='q-item-label', text=text)
