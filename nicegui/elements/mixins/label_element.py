from typing import Any, Callable, Optional, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class LabelElement(Element):
    label = BindableProperty(
        on_change=lambda sender, label: cast(Self, sender)._handle_label_change(label))  # pylint: disable=protected-access

    def __init__(self, *, label: Optional[str], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.label = label
        if label is not None:
            self._props['label'] = label

    def bind_label_to(self,
                      target_object: Any,
                      target_name: str = 'label',
                      forward: Callable[..., Any] = lambda x: x,
                      ) -> Self:
        """Bind the label of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target.
        """
        bind_to(self, 'label', target_object, target_name, forward)
        return self

    def bind_label_from(self,
                        target_object: Any,
                        target_name: str = 'label',
                        backward: Callable[..., Any] = lambda x: x,
                        ) -> Self:
        """Bind the label of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever a value changes.

        :param target_object: The object to bind from.
        :param target_name: The name of the property to bind from.
        :param backward: A function to apply to the value before applying it to this element.
        """
        bind_from(self, 'label', target_object, target_name, backward)
        return self

    def bind_label(self,
                   target_object: Any,
                   target_name: str = 'label', *,
                   forward: Callable[..., Any] = lambda x: x,
                   backward: Callable[..., Any] = lambda x: x,
                   ) -> Self:
        """Bind the label of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.
        The update happens immediately and whenever a value changes.
        The backward binding takes precedence for the initial synchronization.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the value before applying it to the target.
        :param backward: A function to apply to the value before applying it to this element.
        """
        bind(self, 'label', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_label(self, label: Optional[str]) -> None:
        """Set the label of this element.

        :param label: The new label.
        """
        self.label = label

    def _handle_label_change(self, label: Optional[str]) -> None:
        """Called when the label of this element changes.

        :param label: The new label.
        """
        if label is None:
            del self._props['label']
        else:
            self._props['label'] = label
        self.update()
