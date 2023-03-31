from typing import Any, Callable

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class SourceElement(Element):
    source = BindableProperty(on_change=lambda sender, source: sender.on_source_change(source))

    def __init__(self, *, source: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.source = source
        self._props['src'] = source

    def bind_source_to(self,
                       target_object: Any,
                       target_name: str = 'source',
                       forward: Callable = lambda x: x) -> Self:
        """Bind the source of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target.
        """
        bind_to(self, 'source', target_object, target_name, forward)
        return self

    def bind_source_from(self,
                         target_object: Any,
                         target_name: str = 'source',
                         backward: Callable = lambda x: x) -> Self:
        """Bind the source of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.

        :param target_object: The object to bind from.
        :param target_name: The name of the property to bind from.
        :param backward: A function to apply to the value before applying it to this element.
        """
        bind_from(self, 'source', target_object, target_name, backward)
        return self

    def bind_source(self,
                    target_object: Any,
                    target_name: str = 'source', *,
                    forward: Callable = lambda x: x,
                    backward: Callable = lambda x: x) -> Self:
        """Bind the source of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target.
        :param backward: A function to apply to the value before applying it to this element.
        """
        bind(self, 'source', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_source(self, source: str) -> None:
        """Set the source of this element.

        :param source: The new source.
        """
        self.source = source

    def on_source_change(self, source: str) -> None:
        """Called when the source of this element changes.

        :param source: The new source.
        """
        self._props['src'] = source
        self.update()
