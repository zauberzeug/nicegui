from typing import Any, Callable, Optional, Union

from typing_extensions import Self

from ..element import Element
from ..logging import log
from .context_menu import ContextMenu
from .item import Item
from .mixins.value_element import ValueElement


class Menu(ValueElement):

    def __init__(self, *, value: bool = False, auto_close: bool = False) -> None:
        """Menu

        Creates a menu based on Quasar's `QMenu <https://quasar.dev/vue-components/menu>`_ component.
        The menu should be placed inside the element where it should be shown.

        :param value: whether the menu is already opened (default: `False`)
        :param auto_close: whether the menu should be closed after a click on one of its items (default: `False`)
        """
        super().__init__(tag='q-menu', value=value, on_value_change=None)
        if auto_close:
            self._props['auto-close'] = True

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


class MenuItem(Item):

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
        super().__init__(text=text, on_click=on_click)

        self._props['clickable'] = True

        self.menu = self._find_menu()
        if self.menu:
            if not auto_close and self.menu._props.get('auto-close'):
                log.warning('The parameter "auto_close" on this `ui.menu_item` has no effect because the parent '
                            '`ui.menu` is set to "auto_close=True".\n'
                            'Use only the `auto_close` parameter on the `ui.menu_item`s if you want to have different '
                            'behaviors on your `menu_item`s.')
            if auto_close:
                self.on_click(self.menu.close)

    def _find_menu(self) -> Optional[Union[Menu, ContextMenu]]:
        element: Element = self
        while element.parent_slot:
            element = element.parent_slot.parent
            if isinstance(element, (Menu, ContextMenu)):
                return element
        return None
