from pathlib import Path
from typing import Any, Callable, Union

from typing_extensions import Self

from ... import globals
from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element
from ...helpers import is_file


class SourceElement(Element):
    source = BindableProperty(on_change=lambda sender, source: sender.on_source_change(source))

    def __init__(self, *, source: Union[str, Path], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if is_file(source):
            source = globals.app.add_static_file(local_file=source)
        self.source = source
        self._props['src'] = source

    def bind_source_to(self,
                       target_object: Any,
                       target_name: str = 'source',
                       forward: Callable[..., Any] = lambda x: x,
                       ) -> Self:
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
                         backward: Callable[..., Any] = lambda x: x,
                         ) -> Self:
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
                    forward: Callable[..., Any] = lambda x: x,
                    backward: Callable[..., Any] = lambda x: x,
                    ) -> Self:
        """Bind the source of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target.
        :param backward: A function to apply to the value before applying it to this element.
        """
        bind(self, 'source', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_source(self, source: Union[str, Path]) -> None:
        """Set the source of this element.

        :param source: The new source.
        """
        self.source = source

    def on_source_change(self, source: Union[str, Path]) -> None:
        """Called when the source of this element changes.

        :param source: The new source.
        """
        self._props['src'] = source
        self.update()
