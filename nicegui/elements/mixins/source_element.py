from pathlib import Path
from typing import Any, Callable, Optional, Union, cast

from typing_extensions import Self

from ... import core
from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element
from ...helpers import is_file


class SourceElement(Element):
    """
    Represents an element that has a source property.

    The source property can be bound to another object's property, allowing for automatic updates
    whenever the source value changes.

    Usage:
    ```
    element = SourceElement(source='path/to/file.png')
    element.bind_source_to(target_object, target_name='source')
    ```

    Attributes:
        source: The source of the element, which can be a string or a Path object.
        auto_route: The automatically generated route for the source file.
        SOURCE_IS_MEDIA_FILE: A flag indicating whether the source is a media file.

    Methods:
        bind_source_to(target_object, target_name='source', forward=lambda x: x) -> Self:
            Binds the source of this element to the target object's target_name property.
            The binding works one way only, from this element to the target.
            The update happens immediately and whenever a value changes.

        bind_source_from(target_object, target_name='source', backward=lambda x: x) -> Self:
            Binds the source of this element from the target object's target_name property.
            The binding works one way only, from the target to this element.
            The update happens immediately and whenever a value changes.

        bind_source(target_object, target_name='source', forward=lambda x: x, backward=lambda x: x) -> Self:
            Binds the source of this element to the target object's target_name property.
            The binding works both ways, from this element to the target and from the target to this element.
            The update happens immediately and whenever a value changes.
            The backward binding takes precedence for the initial synchronization.

        set_source(source: Union[str, Path]) -> None:
            Sets the source of this element.

        _handle_source_change(source: Union[str, Path]) -> None:
            Called when the source of this element changes.

        _set_props(source: Union[str, Path]) -> None:
            Sets the properties of the element based on the source value.

        _handle_delete() -> None:
            Handles the deletion of the element, removing the auto-generated route if necessary.
    """
    source = BindableProperty(
        on_change=lambda sender, source: cast(Self, sender)._handle_source_change(source))  # pylint: disable=protected-access

    SOURCE_IS_MEDIA_FILE: bool = False

    def __init__(self, *, source: Union[str, Path], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.auto_route: Optional[str] = None
        self.source = source
        self._set_props(source)

    def bind_source_to(self,
                       target_object: Any,
                       target_name: str = 'source',
                       forward: Callable[..., Any] = lambda x: x,
                       ) -> Self:
        """
        Bind the source of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

        Args:
            - target_object: The object to bind to.
            - target_name: The name of the property to bind to.
            - forward: A function to apply to the value before applying it to the target.

        Returns:
            Self: The current instance of the SourceElement.
        """
        bind_to(self, 'source', target_object, target_name, forward)
        return self

    def bind_source_from(self,
                         target_object: Any,
                         target_name: str = 'source',
                         backward: Callable[..., Any] = lambda x: x,
                         ) -> Self:
        """
        Bind the source of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever a value changes.

        Args:
            - target_object: The object to bind from.
            - target_name: The name of the property to bind from.
            - backward: A function to apply to the value before applying it to this element.

        Returns:
            Self: The current instance of the SourceElement.
        """
        bind_from(self, 'source', target_object, target_name, backward)
        return self

    def bind_source(self,
                    target_object: Any,
                    target_name: str = 'source', *,
                    forward: Callable[..., Any] = lambda x: x,
                    backward: Callable[..., Any] = lambda x: x,
                    ) -> Self:
        """
        Bind the source of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.
        The update happens immediately and whenever a value changes.
        The backward binding takes precedence for the initial synchronization.

        Args:
            - target_object: The object to bind to.
            - target_name: The name of the property to bind to.
            - forward: A function to apply to the value before applying it to the target.
            - backward: A function to apply to the value before applying it to this element.

        Returns:
            Self: The current instance of the SourceElement.
        """
        bind(self, 'source', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_source(self, source: Union[str, Path]) -> None:
        """
        Set the source of this element.

        Args:
            - source: The new source.
        """
        self.source = source

    def _handle_source_change(self, source: Union[str, Path]) -> None:
        """
        Called when the source of this element changes.

        Args:
            - source: The new source.
        """
        self._set_props(source)
        self.update()

    def _set_props(self, source: Union[str, Path]) -> None:
        """
        Sets the properties of the element based on the source value.

        Args:
            - source: The source value.
        """
        if is_file(source):
            if self.auto_route:
                core.app.remove_route(self.auto_route)
            if self.SOURCE_IS_MEDIA_FILE:
                source = core.app.add_media_file(local_file=source)
            else:
                source = core.app.add_static_file(local_file=source)
            self.auto_route = source
        self._props['src'] = source

    def _handle_delete(self) -> None:
        """
        Handles the deletion of the element, removing the auto-generated route if necessary.
        """
        if self.auto_route:
            core.app.remove_route(self.auto_route)
        return super()._handle_delete()
