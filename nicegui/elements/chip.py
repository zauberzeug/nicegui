from typing import Any, Callable, List, Optional

from typing_extensions import Self

from ..events import ClickEventArguments, GenericEventArguments, ValueChangeEventArguments, handle_event
from .mixins.color_elements import BackgroundColorElement, TextColorElement
from .mixins.disableable_element import DisableableElement
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Chip(ValueElement, TextElement, BackgroundColorElement, TextColorElement, DisableableElement):
    TEXT_COLOR_PROP = 'text-color'

    def __init__(self,
                 text: str = '',
                 *,
                 icon: Optional[str] = None,
                 selectable: bool = False,
                 removable: bool = False,
                 color: Optional[str] = 'primary',
                 text_color: Optional[str] = None,
                 on_click: Optional[Callable[..., Any]] = None,
                 on_selection_change: Optional[Callable[..., Any]] = None,
                 on_value_change: Optional[Callable[..., Any]] = None,
                 ) -> None:
        """Chip

        A chip element wrapping Quasar's `QChip <https://quasar.dev/vue-components/chip>`_ component. It can be
        clickable, selectable and removable.

        :param text: the initial value of the text field (default: "")
        :param icon: the name of an icon to be displayed on the chip (default: `None`)
        :param selectable: whether the chip is selectable (default: `False`)
        :param removable: whether the chip is removable. Shows a small "x" button if True (default: `False`)
        :param color: the color name for component (either a Quasar, Tailwind, or CSS color or `None`, default: "primary")
        :param text_color: text color (either a Quasar, Tailwind, or CSS color or `None`, default: `None`)
        :param on_click: callback which is invoked when chip is clicked. Makes the chip clickable if set
        :param on_selection_change: callback which is invoked when the chip's selection state is changed
        :param on_value_change: callback which is invoked when the chip is removed or unremoved
        """
        super().__init__(tag='q-chip', value=True, on_value_change=on_value_change,
                         text=text, text_color=text_color, background_color=color)
        if icon:
            self._props['icon'] = icon

        self._props['removable'] = removable

        if on_click:
            self.on_click(on_click)

        self._selection_change_handlers: List[Callable[[ValueChangeEventArguments], Any]] = []
        if selectable:
            self._make_selectable()
        if on_selection_change:
            self.on_selection_change(on_selection_change)

    def on_click(self, callback: Callable[..., Any]) -> Self:
        """Add a callback to be invoked when the chip is clicked."""
        self._props['clickable'] = True
        self.update()
        self.on('click', lambda _: handle_event(callback, ClickEventArguments(sender=self, client=self.client)), [])
        return self

    @property
    def selected(self) -> bool:
        """Whether the chip is selected."""
        return self._props.get('selected', False)

    @selected.setter
    def selected(self, selected: bool):
        """Set whether the chip is selected. Makes the chip selectable."""
        self.set_selected(selected)

    def set_selected(self, selected: bool) -> Self:
        """Set whether the chip is selected. Makes the chip selectable."""
        self._make_selectable()
        if self.selected == selected:
            return self

        self._props['selected'] = selected
        self.update()
        self._handle_selection_change()
        return self

    def on_selection_change(self, callback: Callable[..., Any]) -> Self:
        """Add a callback to be invoked when the chip's selection state changes. Makes the chip selectable."""
        self._make_selectable()
        self._selection_change_handlers.append(callback)
        return self

    def _make_selectable(self) -> None:
        if 'selected' in self._props:
            return  # chip is already selectable

        def handle_selection(e: GenericEventArguments) -> None:
            self._props['selected'] = e.args
            self.update()
            self._handle_selection_change()

        self.on('update:selected', handle_selection)
        self._props['selected'] = False
        self.update()

    def _handle_selection_change(self) -> None:
        args = ValueChangeEventArguments(sender=self, client=self.client, value=self._props['selected'])
        for handler in self._selection_change_handlers:
            handle_event(handler, args)
