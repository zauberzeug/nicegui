from collections.abc import Callable
from typing import Any, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class TextElement(Element):
    text = BindableProperty(
        on_change=lambda sender, text: cast(Self, sender)._handle_text_change(text))  # pylint: disable=protected-access

    def __init__(self, *, text: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.text = text
        self._text_to_model_text(text)

    def bind_text_to(self,
                     target_object: Any,
                     target_name: str = 'text',
                     forward: Callable[[Any], Any] | None = None, *,
                     strict: bool | None = None,
                     ) -> Self:
        """Bind the text of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target (default: identity).
        :param strict: Whether to check (and raise) if the target object has the specified property (default: None,
            performs a check if the object is not a dictionary, *added in version 3.0.0*).
        """
        bind_to(self, 'text', target_object, target_name, forward, self_strict=False, other_strict=strict)
        return self

    def bind_text_from(self,
                       target_object: Any,
                       target_name: str = 'text',
                       backward: Callable[[Any], Any] | None = None, *,
                       strict: bool | None = None,
                       ) -> Self:
        """Bind the text of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind from.
        :param target_name: The name of the property to bind from.
        :param backward: A function to apply to the value before applying it to this element (default: identity).
        :param strict: Whether to check (and raise) if the target object has the specified property (default: None,
            performs a check if the object is not a dictionary, *added in version 3.0.0*).
        """
        bind_from(self, 'text', target_object, target_name, backward, self_strict=False, other_strict=strict)
        return self

    def bind_text(self,
                  target_object: Any,
                  target_name: str = 'text', *,
                  forward: Callable[[Any], Any] | None = None,
                  backward: Callable[[Any], Any] | None = None,
                  strict: bool | None = None,
                  ) -> Self:
        """Bind the text of this element to the target object's target_name property.

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
        bind(self, 'text', target_object, target_name,
             forward=forward, backward=backward,
             self_strict=False, other_strict=strict)
        return self

    def set_text(self, text: str) -> None:
        """Set the text of this element.

        :param text: The new text.
        """
        self.text = text

    def _handle_text_change(self, text: str) -> None:
        """Called when the text of this element changes.

        :param text: The new text.
        """
        self._text_to_model_text(text)
        self.update()

    def _text_to_model_text(self, text: str) -> None:
        self._text = text
