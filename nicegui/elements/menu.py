from typing import Any, Callable, Optional

from typing_extensions import Self

from .. import context
from ..events import ClickEventArguments, handle_event
from ..logging import log
from .context_menu import ContextMenu
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Menu(ValueElement):

    def __init__(self, *, value: bool = False) -> None:
        """Menu

        Creates a menu based on Quasar's `QMenu <https://quasar.dev/vue-components/menu>`_ component.
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

    def props(self, add: Optional[str] = None, *, remove: Optional[str] = None) -> Self:
        super().props(add, remove=remove)
        if 'touch-position' in self._props:
            # https://github.com/zauberzeug/nicegui/issues/1738
            del self._props['touch-position']
            log.warning('The prop "touch-position" is not supported by `ui.menu`.\n'
                        'Use "ui.context_menu()" instead.')
        return self


class MenuItem(TextElement):

    def __init__(self,
                 text: str = '',
                 on_click: Optional[Callable[..., Any]] = None, *,
                 auto_close: bool = True,
                 ) -> None:
        """Menu Item

        A menu item to be added to a menu.
        This element is based on Quasar's `QItem <https://quasar.dev/vue-components/list-and-list-items#qitem-api>`_ component.

        :param text: label of the menu item
        :param on_click: callback to be executed when selecting the menu item
        :param auto_close: whether the menu should be closed after a click event (default: `True`)
        """
        super().__init__(tag='q-item', text=text)
        self.menu = context.get_slot().parent
        self._props['clickable'] = True

        def handle_click(_) -> None:
            handle_event(on_click, ClickEventArguments(sender=self, client=self.client))
            if auto_close:
                assert isinstance(self.menu, (Menu, ContextMenu))
                self.menu.close()
        self.on('click', handle_click, [])
