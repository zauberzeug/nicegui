from typing import Any, Callable, Optional, cast

from typing_extensions import Self

from nicegui.binding import BindableProperty, bind, bind_from, bind_to

from ...element import Element

QUASAR_COLORS = {'primary', 'secondary', 'accent', 'dark', 'positive', 'negative', 'info', 'warning'}
for color in ['red', 'pink', 'purple', 'deep-purple', 'indigo', 'blue', 'light-blue', 'cyan', 'teal', 'green',
              'light-green', 'lime', 'yellow', 'amber', 'orange', 'deep-orange', 'brown', 'grey', 'blue-grey']:
    QUASAR_COLORS.add(color)
    for i in range(1, 15):
        QUASAR_COLORS.add(f'{color}-{i}')

TAILWIND_COLORS = {
    f'{name}-{value}'
    for name in ['red', 'orange', 'amber', 'yellow', 'lime', 'green', 'emerald', 'teal', 'cyan', 'sky', 'blue',
                 'indigo', 'violet', 'purple', 'fuchsia', 'pink', 'rose', 'slate', 'gray', 'zinc', 'neutral', 'stone']
    for value in [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]
}


class BackgroundColorElement(Element):
    BACKGROUND_COLOR_PROP = 'color'
    background_color = BindableProperty(
        on_change=lambda sender, background_color: cast(Self, sender)._handle_background_color_change(background_color))  # pylint: disable=protected-access

    def __init__(self, *, background_color: Optional[str], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.background_color = background_color
        self._handle_background_color_change(background_color, _skip_clear=True)

    def set_background_color(self, background_color: Optional[str]) -> None:
        """Sets the background color"""
        self.background_color = background_color

    def _handle_background_color_change(self, background_color: Optional[str], _skip_clear: bool = False) -> None:
        if not _skip_clear:
            self._clear_background_color()
        if background_color in QUASAR_COLORS:
            self._props[self.BACKGROUND_COLOR_PROP] = background_color
        elif background_color in TAILWIND_COLORS:
            self._classes.append(f'bg-{background_color}')
        elif background_color is not None:
            self._style['background-color'] = background_color

    def _clear_background_color(self) -> None:
        """Clears the background color"""
        self._props.pop(self.BACKGROUND_COLOR_PROP, None)
        self._classes(remove=' '.join(f'bg-{t}' for t in TAILWIND_COLORS))
        self._style.pop('background-color', None)

    def bind_background_color_to(self,
                                 target_object: Any,
                                 target_name: str = 'background_color',
                                 forward: Optional[Callable[[Any], Any]] = None, *,
                                 strict: Optional[bool] = None,
                                 ) -> Self:
        """Bind the background color of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target (default: identity).
        :param strict: Whether to check (and raise) if the target object has the specified property (default: None,
            performs a check if the object is not a dictionary, *added in version 3.0.0*).
        """
        bind_to(self, 'background_color', target_object, target_name, forward, self_strict=False, other_strict=strict)
        return self

    def bind_background_color_from(self,
                                   target_object: Any,
                                   target_name: str = 'background_color',
                                   backward: Optional[Callable[[Any], Any]] = None, *,
                                   strict: Optional[bool] = None,
                                   ) -> Self:
        """Bind the background color of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind from.
        :param target_name: The name of the property to bind from.
        :param backward: A function to apply to the value before applying it to this element (default: identity).
        :param strict: Whether to check (and raise) if the target object has the specified property (default: None,
            performs a check if the object is not a dictionary, *added in version 3.0.0*).
        """
        bind_from(self, 'background_color', target_object, target_name,
                  backward, self_strict=False, other_strict=strict)
        return self

    def bind_background_color(self,
                              target_object: Any,
                              target_name: str = 'background_color', *,
                              forward: Optional[Callable[[Any], Any]] = None,
                              backward: Optional[Callable[[Any], Any]] = None,
                              strict: Optional[bool] = None,
                              ) -> Self:
        """Bind the background color of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.
        The update happens immediately and whenever a value changes.
        The backward binding takes precedence for the initial synchronization.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target (default: identity).
        :param backward: A function to apply to the value before applying it to this element (default: identity).
        :param strict: Whether to check (and raise) if the target object has the specified property (default: None,
            performs a check if the object is not a dictionary, *added in version 3.0.0*).
        """
        bind(self, 'background_color', target_object, target_name,
             forward=forward, backward=backward,
             self_strict=False, other_strict=strict)
        return self


class TextColorElement(Element):
    TEXT_COLOR_PROP = 'color'

    text_color = BindableProperty(
        on_change=lambda sender, text_color: cast(Self, sender)._handle_text_color_change(text_color))  # pylint: disable=protected-access

    def __init__(self, *, text_color: Optional[str], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.text_color = text_color
        self._handle_text_color_change(text_color, _skip_clear=True)

    def set_text_color(self, text_color: Optional[str]) -> None:
        """Sets the text color"""
        self.text_color = text_color

    def _handle_text_color_change(self, text_color: Optional[str], _skip_clear: bool = False) -> None:
        if not _skip_clear:
            self._clear_text_color()
        if text_color in QUASAR_COLORS:
            self._props[self.TEXT_COLOR_PROP] = text_color
        elif text_color in TAILWIND_COLORS:
            self._classes.append(f'text-{text_color}')
        elif text_color is not None:
            self._style['color'] = text_color

    def _clear_text_color(self) -> None:
        """Clears the text color"""
        self._props.pop(self.TEXT_COLOR_PROP, None)
        self._classes(remove=' '.join(f'text-{t}' for t in TAILWIND_COLORS))
        self._style.pop('color', None)

    def bind_text_color_to(self,
                           target_object: Any,
                           target_name: str = 'text_color',
                           forward: Optional[Callable[[Any], Any]] = None, *,
                           strict: Optional[bool] = None,
                           ) -> Self:
        """Bind the text color of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target (default: identity).
        :param strict: Whether to check (and raise) if the target object has the specified property (default: None,
            performs a check if the object is not a dictionary, *added in version 3.0.0*).
        """
        bind_to(self, 'text_color', target_object, target_name, forward, self_strict=False, other_strict=strict)
        return self

    def bind_text_color_from(self,
                             target_object: Any,
                             target_name: str = 'text_color',
                             backward: Optional[Callable[[Any], Any]] = None, *,
                             strict: Optional[bool] = None,
                             ) -> Self:
        """Bind the text color of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind from.
        :param target_name: The name of the property to bind from.
        :param backward: A function to apply to the value before applying it to this element (default: identity).
        :param strict: Whether to check (and raise) if the target object has the specified property (default: None,
            performs a check if the object is not a dictionary, *added in version 3.0.0*).
        """
        bind_from(self, 'text_color', target_object, target_name,
                  backward, self_strict=False, other_strict=strict)
        return self

    def bind_text_color(self,
                        target_object: Any,
                        target_name: str = 'text_color', *,
                        forward: Optional[Callable[[Any], Any]] = None,
                        backward: Optional[Callable[[Any], Any]] = None,
                        strict: Optional[bool] = None,
                        ) -> Self:
        """Bind the text color of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.
        The update happens immediately and whenever a value changes.
        The backward binding takes precedence for the initial synchronization.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target (default: identity).
        :param backward: A function to apply to the value before applying it to this element (default: identity).
        :param strict: Whether to check (and raise) if the target object has the specified property (default: None,
              performs a check if the object is not a dictionary, *added in version 3.0.0*).
        """
        bind(self, 'text_color', target_object, target_name,
             forward=forward, backward=backward,
             self_strict=False, other_strict=strict)
        return self
