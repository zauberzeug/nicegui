from typing import Any, Callable, Optional

from .. import globals
from ..events import ClickEventArguments, handle_event
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Menu(ValueElement):

    def __init__(self, *, value: bool = False) -> None:
        """Menu

        Creates a menu.
        The menu should be placed inside the element where it should be shown.

        :param value: whether the menu is already opened (default: `False`)
        """
        super().__init__(tag='q-menu', value=value, on_value_change=None)

    def open(self) -> None:
        """Open the menu."""
        self.value = True

    def close(self) -> None:
        """Close the menu."""
        self.value = False

    def toggle(self) -> None:
        """Toggle the menu."""
        self.value = not self.value


class MenuItem(TextElement):

    def __init__(self,
                 text: str = '',
                 on_click: Optional[Callable[..., Any]] = None, *,
                 auto_close: bool = True,
                 ) -> None:
        """Menu Item

        A menu item to be added to a menu.

        :param text: label of the menu item
        :param on_click: callback to be executed when selecting the menu item
        :param auto_close: whether the menu should be closed after a click event (default: `True`)
        """
        super().__init__(tag='q-item', text=text)
        self.menu = globals.get_slot().parent
        self._props['clickable'] = True

        def handle_click(_) -> None:
            handle_event(on_click, ClickEventArguments(sender=self, client=self.client))
            if auto_close:
                assert isinstance(self.menu, Menu)
                self.menu.close()
        self.on('click', handle_click, [])
