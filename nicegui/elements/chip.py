from typing import Optional

from typing_extensions import Self

from ..events import ClickEventArguments, Handler, ValueChangeEventArguments, handle_event
from .mixins.color_elements import BackgroundColorElement, TextColorElement
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.selectable_element import SelectableElement
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Chip(IconElement, ValueElement, TextElement, BackgroundColorElement, TextColorElement, DisableableElement, SelectableElement):
    TEXT_COLOR_PROP = 'text-color'

    def __init__(self,
                 text: str = '',
                 *,
                 icon: Optional[str] = None,
                 color: Optional[str] = 'primary',
                 text_color: Optional[str] = None,
                 on_click: Optional[Handler[ClickEventArguments]] = None,
                 selectable: bool = False,
                 selected: bool = False,
                 on_selection_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 removable: bool = False,
                 on_value_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """Chip

        A chip element wrapping Quasar's `QChip <https://quasar.dev/vue-components/chip>`_ component.
        It can be clickable, selectable and removable.

        :param text: the initial value of the text field (default: "")
        :param icon: the name of an icon to be displayed on the chip (default: `None`)
        :param color: the color name for component (either a Quasar, Tailwind, or CSS color or `None`, default: "primary")
        :param text_color: text color (either a Quasar, Tailwind, or CSS color or `None`, default: `None`)
        :param on_click: callback which is invoked when chip is clicked. Makes the chip clickable if set
        :param selectable: whether the chip is selectable (default: `False`)
        :param selected: whether the chip is selected (default: `False`)
        :param on_selection_change: callback which is invoked when the chip's selection state is changed
        :param removable: whether the chip is removable. Shows a small "x" button if True (default: `False`)
        :param on_value_change: callback which is invoked when the chip is removed or unremoved
        """
        super().__init__(tag='q-chip', value=True, on_value_change=on_value_change,
                         icon=icon, text=text, text_color=text_color, background_color=color,
                         selectable=selectable, selected=selected, on_selection_change=on_selection_change)

        self._props['removable'] = removable

        if on_click:
            self.on_click(on_click)

    def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
        """Add a callback to be invoked when the chip is clicked."""
        self._props['clickable'] = True
        self.update()
        self.on('click', lambda _: handle_event(callback, ClickEventArguments(sender=self, client=self.client)), [])
        return self
