from typing import Any, Callable

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class ContentElement(Element):
    content = BindableProperty(on_change=lambda sender, content: sender.on_content_change(content))

    def __init__(self, *, content: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.content = content
        self.on_content_change(content)

    def bind_content_to(self, target_object: Any, target_name: str = 'content', forward: Callable = lambda x: x):
        bind_to(self, 'content', target_object, target_name, forward)
        return self

    def bind_content_from(self, target_object: Any, target_name: str = 'content', backward: Callable = lambda x: x):
        bind_from(self, 'content', target_object, target_name, backward)
        return self

    def bind_content(self, target_object: Any, target_name: str = 'content', *,
                     forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        bind(self, 'content', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_content(self, content: str) -> None:
        self.content = content

    def on_content_change(self, content: str) -> None:
        if '</script>' in content:
            raise ValueError('HTML elements must not contain <script> tags. Use ui.add_body_html() instead.')
        self._props['innerHTML'] = content
        self.update()
