from collections.abc import Callable
from typing import Any, Literal, cast

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

    def __init__(self, *, background_color: str | None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._background_color_state: tuple[Literal[None, 'prop', 'class', 'style'], str] = (None, '')
        self.background_color = background_color
        self._handle_background_color_change(background_color)

    def set_background_color(self, background_color: str | None) -> None:
        """Set the background color of this element."""
        self.background_color = background_color

    def _handle_background_color_change(self, background_color: str | None) -> None:
        # Clear previous color based on tracked state
        color_type, value = self._background_color_state
        if color_type == 'prop':
            self._props.pop(self.BACKGROUND_COLOR_PROP, None)
        elif color_type == 'class':
            self._classes.remove(f'bg-{value}')
        elif color_type == 'style':
            self._style.pop('background-color', None)

        # Set new color and track state
        if background_color in QUASAR_COLORS or background_color is None:
            self._props.set_optional(self.BACKGROUND_COLOR_PROP, background_color)
            self._background_color_state = ('prop', background_color) if background_color else (None, '')
        elif background_color in TAILWIND_COLORS:
            self._classes.append(f'bg-{background_color}')
            self._background_color_state = ('class', background_color)
        else:
            self._style['background-color'] = background_color
            self._background_color_state = ('style', background_color)

    def bind_background_color_to(self,
                                 target_object: Any,
                                 target_name: str = 'background_color',
                                 forward: Callable[[Any], Any] | None = None, *,
                                 strict: bool | None = None,
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
                                   backward: Callable[[Any], Any] | None = None, *,
                                   strict: bool | None = None,
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
                              forward: Callable[[Any], Any] | None = None,
                              backward: Callable[[Any], Any] | None = None,
                              strict: bool | None = None,
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

    def __init__(self, *, text_color: str | None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._text_color_state: tuple[Literal[None, 'prop', 'class', 'style'], str] = (None, '')
        self.text_color = text_color
        self._handle_text_color_change(text_color)

    def set_text_color(self, text_color: str | None) -> None:
        """Set the text color of this element."""
        self.text_color = text_color

    def _handle_text_color_change(self, text_color: str | None) -> None:
        # Clear previous color based on tracked state
        color_type, value = self._text_color_state
        if color_type == 'prop':
            self._props.pop(self.TEXT_COLOR_PROP, None)
        elif color_type == 'class':
            self._classes.remove(f'text-{value}')
        elif color_type == 'style':
            self._style.pop('color', None)

        # Set new color and track state
        if text_color in QUASAR_COLORS or text_color is None:
            self._props.set_optional(self.TEXT_COLOR_PROP, text_color)
            self._text_color_state = ('prop', text_color) if text_color else (None, '')
        elif text_color in TAILWIND_COLORS:
            self._classes.append(f'text-{text_color}')
            self._text_color_state = ('class', text_color)
        else:
            self._style['color'] = text_color
            self._text_color_state = ('style', text_color)

    def bind_text_color_to(self,
                           target_object: Any,
                           target_name: str = 'text_color',
                           forward: Callable[[Any], Any] | None = None, *,
                           strict: bool | None = None,
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
                             backward: Callable[[Any], Any] | None = None, *,
                             strict: bool | None = None,
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
                        forward: Callable[[Any], Any] | None = None,
                        backward: Callable[[Any], Any] | None = None,
                        strict: bool | None = None,
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
