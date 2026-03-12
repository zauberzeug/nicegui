from typing_extensions import Self

from ..defaults import DEFAULT_PROP, resolve_defaults
from ..events import ClickEventArguments, Handler, ValueChangeEventArguments, handle_event
from .mixins.color_elements import BackgroundColorElement
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class DropdownButton(IconElement, TextElement, DisableableElement, BackgroundColorElement, ValueElement):

    @resolve_defaults
    def __init__(self,
                 text: str = '', *,
                 value: bool = False,
                 on_value_change: Handler[ValueChangeEventArguments] | None = None,
                 on_click: Handler[ClickEventArguments] | None = None,
                 color: str | None = DEFAULT_PROP | 'primary',
                 icon: str | None = DEFAULT_PROP | None,
                 auto_close: bool | None = DEFAULT_PROP | False,
                 split: bool | None = DEFAULT_PROP | False,
                 ) -> None:
        """Dropdown Button

        This element is based on Quasar's `QBtnDropDown <https://quasar.dev/vue-components/button-dropdown>`_ component.

        The ``color`` parameter accepts a Quasar color, a Tailwind color, or a CSS color.
        If a Quasar color is used, the button will be styled according to the Quasar theme including the color of the text.
        Note that there are colors like "red" being both a Quasar color and a CSS color.
        In such cases the Quasar color will be used.

        :param text: the label of the button
        :param value: if the dropdown is open or not (default: `False`)
        :param on_value_change: callback which is invoked when the dropdown is opened or closed
        :param on_click: callback which is invoked when button is pressed
        :param color: the color of the button (either a Quasar, Tailwind, or CSS color or `None`, default: 'primary')
        :param icon: the name of an icon to be displayed on the button (default: `None`)
        :param auto_close: whether the dropdown should close automatically when an item is clicked (default: `False`)
        :param split: whether to split the dropdown icon into a separate button (default: `False`)
        """
        super().__init__(tag='q-btn-dropdown',
                         icon=icon, text=text, background_color=color, value=value, on_value_change=on_value_change)

        self._props.set_bool('auto-close', auto_close)
        self._props.set_bool('split', split)

        if on_click:
            self.on_click(on_click)

    def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
        """Add a callback to be invoked when the dropdown button is clicked.

        *Added in version 2.22.0*
        """
        self.on('click', lambda _: handle_event(callback, ClickEventArguments(sender=self, client=self.client)), [])
        return self

    def _text_to_model_text(self, text: str) -> None:
        self._props['label'] = text

    def open(self) -> None:
        """Open the dropdown."""
        self.value = True

    def close(self) -> None:
        """Close the dropdown."""
        self.value = False

    def toggle(self) -> None:
        """Toggle the dropdown."""
        self.value = not self.value
