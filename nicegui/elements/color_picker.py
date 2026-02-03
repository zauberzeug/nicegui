from typing_extensions import Self

from ..defaults import DEFAULT_PROPS, resolve_defaults
from ..element import Element
from ..events import ColorPickEventArguments, GenericEventArguments, Handler, handle_event
from .menu import Menu


class ColorPicker(Menu):

    @resolve_defaults
    def __init__(self, *,
                 on_pick: Handler[ColorPickEventArguments] | None = None,
                 value: bool = DEFAULT_PROPS['model-value'] | False,
                 ) -> None:
        """Color Picker

        This element is based on Quasar's `QMenu <https://quasar.dev/vue-components/menu>`_ and
        `QColor <https://quasar.dev/vue-components/color-picker>`_ components.

        :param on_pick: callback to execute when a color is picked
        :param value: whether the menu is already opened (default: `False`)
        """
        super().__init__(value=value)
        self._pick_handlers = [on_pick] if on_pick else []
        with self:
            def handle_change(e: GenericEventArguments):
                for handler in self._pick_handlers:
                    handle_event(handler, ColorPickEventArguments(sender=self, client=self.client, color=e.args))
            self.q_color = Element('q-color').on('change', handle_change)

    def set_color(self, color: str) -> None:
        """Set the color of the picker.

        :param color: the color to set
        """
        self.q_color.props(f'model-value="{color}"')

    def on_pick(self, callback: Handler[ColorPickEventArguments]) -> Self:
        """Add a callback to be invoked when a color is picked."""
        self._pick_handlers.append(callback)
        return self
