from pathlib import Path
from typing import Any, Callable, Optional, cast

from typing_extensions import Self

from ... import core
from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element
from ...helpers import is_file


class SourceElement(Element):
    source = BindableProperty(
        on_change=lambda sender, source: cast(Self, sender)._handle_source_change(source))  # pylint: disable=protected-access

    SOURCE_IS_MEDIA_FILE: bool = False

    def __init__(self, *, source: Any, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.auto_route: Optional[str] = None
        self.source = source
        self._set_props(source)

    def bind_source_to(self,
                       target_object: Any,
                       target_name: str = 'source',
                       forward: Callable[..., Any] = lambda x: x,
                       ) -> Self:
        """Bind the source of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

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
        The update happens immediately and whenever a value changes.

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
        The update happens immediately and whenever a value changes.
        The backward binding takes precedence for the initial synchronization.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target.
        :param backward: A function to apply to the value before applying it to this element.
        """
        bind(self, 'source', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_source(self, source: Any) -> None:
        """Set the source of this element.

        :param source: The new source.
        """
        self.source = source

    def _handle_source_change(self, source: Any) -> None:
        """Called when the source of this element changes.

        :param source: The new source.
        """
        self._set_props(source)
        self.update()

    def _set_props(self, source: Any) -> None:
        if is_file(source):
            if self.auto_route:
                core.app.remove_route(self.auto_route)
            if self.SOURCE_IS_MEDIA_FILE:
                source = core.app.add_media_file(local_file=source)
            else:
                source = core.app.add_static_file(local_file=source)
            self.auto_route = source
        if isinstance(source, Path) and not source.exists():
            raise FileNotFoundError(f'File not found: {source}')
        self._props['src'] = source

    def _handle_delete(self) -> None:
        if self.auto_route:
            core.app.remove_route(self.auto_route)
        return super()._handle_delete()
