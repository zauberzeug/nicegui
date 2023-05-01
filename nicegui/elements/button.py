from typing import Callable, Optional

from ..colors import set_background_color
from ..events import ClickEventArguments, handle_event
from .mixins.disableable_element import DisableableElement
from .mixins.text_element import TextElement


class Button(TextElement, DisableableElement):

    def __init__(self,
                 text: str = '', *,
                 on_click: Optional[Callable] = None,
                 color: Optional[str] = 'primary',
                 ) -> None:
        """Button

        This element is based on Quasar's `QBtn <https://quasar.dev/vue-components/button>`_ component.

        The ``color`` parameter excepts a Quasar color, a Tailwind color, or a CSS color.
        If a Quasar color is used, the button will be styled according to the Quasar theme including the color of the text.
        Note that there are colors like "red" being both a Quasar color and a CSS color.
        In such cases the Quasar color will be used.

        :param text: the label of the button
        :param on_click: callback which is invoked when button is pressed
        :param color: the color of the button (either a Quasar, Tailwind, or CSS color or `None`, default: 'primary')
        """
        super().__init__(tag='q-btn', text=text)
        set_background_color(self, color)

        if on_click:
            self.on('click', lambda _: handle_event(on_click, ClickEventArguments(sender=self, client=self.client)))

    def _text_to_model_text(self, text: str) -> None:
        self._props['label'] = text
