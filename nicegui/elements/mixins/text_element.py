from typing import Any, Callable

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class TextElement(Element):
    text = BindableProperty(on_change=lambda sender, text: sender.on_text_change(text))

    def __init__(self, *, text: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.text = text
        self._text_to_model_text(text)

    def bind_text_to(self, target_object: Any, target_name: str = 'text', forward: Callable = lambda x: x):
        bind_to(self, 'text', target_object, target_name, forward)
        return self

    def bind_text_from(self, target_object: Any, target_name: str = 'text', backward: Callable = lambda x: x):
        bind_from(self, 'text', target_object, target_name, backward)
        return self

    def bind_text(self, target_object: Any, target_name: str = 'text', *,
                  forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        bind(self, 'text', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_text(self, text: str) -> None:
        self.text = text

    def on_text_change(self, text: str) -> None:
        self._text_to_model_text(text)
        self.update()

    def _text_to_model_text(self, text: str) -> None:
        self._text = text
