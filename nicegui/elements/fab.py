from typing import Literal

from typing_extensions import Self

from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import ClickEventArguments, Handler, handle_event
from .mixins.color_elements import BackgroundColorElement
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.label_element import LabelElement
from .mixins.value_element import ValueElement


class Fab(ValueElement, LabelElement, IconElement, BackgroundColorElement, DisableableElement):

    @resolve_defaults
    def __init__(self,
                 icon: str, *,
                 value: bool = DEFAULT_PROPS['model-value'] | False,
                 label: str = DEFAULT_PROP | '',
                 color: str | None = DEFAULT_PROP | 'primary',
                 direction: Literal['up', 'down', 'left', 'right'] = DEFAULT_PROP | 'right',
                 ) -> None:
        """Floating Action Button (FAB)

        A floating action button that can be used to trigger an action.
        This element is based on Quasar's `QFab <https://quasar.dev/vue-components/floating-action-button#qfab-api>`_ component.

        :param icon: icon to be displayed on the FAB
        :param value: whether the FAB is already opened (default: ``False``)
        :param label: optional label for the FAB
        :param color: background color of the FAB (default: "primary")
        :param direction: direction of the FAB ("up", "down", "left", "right", default: "right")
        """
        super().__init__(tag='q-fab', value=value, label=label, background_color=color, icon=icon)
        self._props['direction'] = direction

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

    @resolve_defaults
    def __init__(self,
                 icon: str, *,
                 label: str = DEFAULT_PROP | '',
                 on_click: Handler[ClickEventArguments] | None = None,
                 color: str | None = DEFAULT_PROP | 'primary',
                 auto_close: bool = True,
                 ) -> None:
        """Floating Action Button Action

        An action that can be added to a floating action button (FAB).
        This element is based on Quasar's `QFabAction <https://quasar.dev/vue-components/floating-action-button#qfabaction-api>`_ component.

        *Added in version 2.22.0*

        :param icon: icon to be displayed on the action button
        :param label: optional label for the action button
        :param color: background color of the action button (default: "primary")
        :param auto_close: whether the FAB should be closed after a click event (default: ``True``)
        """
        super().__init__(tag='q-fab-action', label=label, background_color=color, icon=icon)
        self.fab = next((e for e in self.ancestors() if isinstance(e, Fab)), None)
        if self.fab and not auto_close:
            self.on('click', self.fab.open)

        if on_click:
            self.on_click(on_click)

    def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
        """Add a callback to be invoked when the action element is clicked."""
        self.on('click', lambda _: handle_event(callback, ClickEventArguments(sender=self, client=self.client)), [])
        return self
