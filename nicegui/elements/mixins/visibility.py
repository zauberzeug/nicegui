from typing import TYPE_CHECKING, Any, Callable

from ...binding import BindableProperty, bind, bind_from, bind_to

if TYPE_CHECKING:
    from ...element import Element


class Visibility:
    visible = BindableProperty(on_change=lambda sender, visible: sender.on_visibility_change(visible))

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.visible = True

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

    def on_visibility_change(self: 'Element', visible: str) -> None:
        if visible and 'hidden' in self._classes:
            self._classes.remove('hidden')
            self.update()
        if not visible and 'hidden' not in self._classes:
            self._classes.append('hidden')
            self.update()
