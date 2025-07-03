from typing import Optional

from nicegui.element import Element

from .mixins.color_elements import BackgroundColorElement
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.label_element import LabelElement
from .mixins.value_element import ValueElement


class Fab(ValueElement, LabelElement, IconElement, BackgroundColorElement, DisableableElement):

    def __init__(self, icon: str, *, value: bool = False, label: str = '', color: Optional[str] = 'primary') -> None:
        """Floating Action Button (FAB)

        A floating action button that can be used to trigger an action.
        This element is based on Quasar's `QFab <https://quasar.dev/vue-components/floating-action-button#qfab-api>`_ component.

        :param icon: icon to be displayed on the FAB
        :param value: whether the FAB is already opened (default: `False`)
        :param label: optional label for the FAB
        :param color: background color of the FAB (default: `primary`)
        """
        super().__init__(tag='q-fab', value=value, label=label, background_color=color, icon=icon)

    def open(self) -> None:
        """Open the FAB."""
        self.value = True

    def close(self) -> None:
        """Close the FAB."""
        self.value = False

    def toggle(self) -> None:
        """Toggle the FAB."""
        self.value = not self.value


class FabAction(LabelElement, IconElement, BackgroundColorElement, DisableableElement):

    def __init__(self, icon: str, *, text: str = '', color: Optional[str] = 'primary', auto_close: bool = True) -> None:
        """Floating Action Button Action

        An action that can be added to a floating action button.
        This element is based on Quasar's `QFabAction <https://quasar.dev/vue-components/floating-action-button#qfabaction-api>`_ component.

        :param icon: icon to be displayed on the action button
        :param text: optional text for the action button
        :param color: background color of the action button (default: `primary`)
        :param auto_close: whether the FAB should be closed after a click event (default: `True`)
        """
        super().__init__(tag='q-fab-action', label=text, background_color=color, icon=icon)
        self.fab = self._find_fab()
        if self.fab and auto_close:
            self.on('click', self.fab.close)

    def _find_fab(self) -> Optional[Fab]:
        """Find the closest FAB ancestor element."""
        element: Element = self
        while element.parent_slot:
            element = element.parent_slot.parent
            if isinstance(element, Fab):
                return element
        return None
