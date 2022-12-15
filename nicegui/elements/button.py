from typing import Callable, Optional

from ..events import ClickEventArguments, handle_event
from .mixins.text_element import TextElement


class Button(TextElement):

    def __init__(self, text: str = '', *, on_click: Optional[Callable] = None) -> None:
        """Button

        :param text: the label of the button
        :param on_click: callback which is invoked when button is pressed
        """
        super().__init__(tag='q-btn', text=text)
        self._props['color'] = 'primary'

        self.on('click', lambda _: handle_event(on_click, ClickEventArguments(sender=self, client=self.client)))

    def _text_to_model_text(self, text: str) -> None:
        self._props['label'] = text
