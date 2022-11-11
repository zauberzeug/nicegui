from typing import Any, Callable

from ..binding import BindableProperty, bind, bind_from, bind_to


class BindTextMixin:
    """
    Mixin providing bind methods for attribute text.
    """
    text = BindableProperty(on_change=lambda sender, text: sender.on_text_change(text))

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
        pass


class BindValueMixin:
    """
    Mixin providing bind methods for attribute value.
    """
    value = BindableProperty(on_change=lambda sender, value: sender.on_value_change(value))

    def bind_value_to(self, target_object: Any, target_name: str = 'value', forward: Callable = lambda x: x):
        bind_to(self, 'value', target_object, target_name, forward)
        return self

    def bind_value_from(self, target_object: Any, target_name: str = 'value', backward: Callable = lambda x: x):
        bind_from(self, 'value', target_object, target_name, backward)
        return self

    def bind_value(self, target_object: Any, target_name: str = 'value', *,
                   forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        bind(self, 'value', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_value(self, value: str) -> None:
        self.value = value

    def on_value_change(self, value: str) -> None:
        pass


class BindContentMixin:
    """
    Mixin providing bind methods for attribute content.
    """
    content = BindableProperty(on_change=lambda sender, content: sender.on_content_change(content))

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
        pass


class BindVisibilityMixin:
    """
    Mixin providing bind methods for attribute visible.
    """
    visible = BindableProperty(on_change=lambda sender, visible: sender.on_visibility_change(visible))

    def bind_visibility_to(self, target_object: Any, target_name: str = 'visible', forward: Callable = lambda x: x):
        bind_to(self, 'visible', target_object, target_name, forward)
        return self

    def bind_visibility_from(self, target_object: Any, target_name: str = 'visible',
                             backward: Callable = lambda x: x, *, value: Any = None):
        if value is not None:
            def backward(x): return x == value
        bind_from(self, 'visible', target_object, target_name, backward)
        return self

    def bind_visibility(self, target_object: Any, target_name: str = 'visible', *,
                        forward: Callable = lambda x: x, backward: Callable = lambda x: x, value: Any = None):
        if value is not None:
            def backward(x): return x == value
        bind(self, 'visible', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_visibility(self, visible: str) -> None:
        self.visible = visible

    def on_visibility_change(self, visible: str) -> None:
        pass


class BindSourceMixin:
    """
    Mixin providing bind methods for attribute source.
    """
    source = BindableProperty(on_change=lambda sender, source: sender.on_source_change(source))

    def bind_source_to(self, target_object: Any, target_name: str = 'source', forward: Callable = lambda x: x):
        bind_to(self, 'source', target_object, target_name, forward)
        return self

    def bind_source_from(self, target_object: Any, target_name: str = 'source', backward: Callable = lambda x: x):
        bind_from(self, 'source', target_object, target_name, backward)
        return self

    def bind_source(self, target_object: Any, target_name: str = 'source', *,
                    forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        bind(self, 'source', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_source(self, source: str) -> None:
        self.source = source

    def on_source_change(self, source: str) -> None:
        pass
