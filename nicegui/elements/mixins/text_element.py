from typing import Any, Callable, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class TextElement(Element):
    """
    A mixin class for elements that display text.

    This class provides functionality for binding the text of an element to a target object's property,
    as well as setting and handling changes to the text.

    Usage:
    1. Inherit from `TextElement` when creating a new element class that needs to display text.
    2. Use the `text` property to get or set the text of the element.
    3. Use the `bind_text_to`, `bind_text_from`, or `bind_text` methods to establish a binding between
       the text of the element and a target object's property.
    4. Use the `set_text` method to set the text of the element.
    5. Override the `_handle_text_change` method to perform custom actions when the text of the element changes.

    Example:
    ```python
    class MyLabel(TextElement):
        def __init__(self, text: str, **kwargs: Any) -> None:
            super().__init__(**kwargs)
            self.text = text

    label = MyLabel(text="Hello, World!")
    label.bind_text_to(target_object=my_object, target_name="name")
    ```

    Attributes:
    - text: The text displayed by the element.

    Methods:
    - bind_text_to: Bind the text of the element to a target object's property.
    - bind_text_from: Bind the text of the element from a target object's property.
    - bind_text: Bind the text of the element to and from a target object's property.
    - set_text: Set the text of the element.
    - _handle_text_change: Called when the text of the element changes.

    """

    text = BindableProperty(
        on_change=lambda sender, text: cast(Self, sender)._handle_text_change(text))  # pylint: disable=protected-access

    def __init__(self, *, text: str, **kwargs: Any) -> None:
        """
        Initialize the TextElement.

        Args:
        - text (str): The initial text of the element.
        - **kwargs (Any): Additional keyword arguments to pass to the parent class.

        Returns:
        - None

        Raises:
        - None

        Examples:
        >>> element = TextElement(text="Hello, world!")
        >>> element.text
        'Hello, world!'
        """
        super().__init__(**kwargs)
        self.text = text
        self._text_to_model_text(text)

    def bind_text_to(self,
                     target_object: Any,
                     target_name: str = 'text',
                     forward: Callable[..., Any] = lambda x: x,
                     ) -> Self:
        """
        Bind the text of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

        Args:
        - target_object: The object to bind to.
        - target_name: The name of the property to bind to.
        - forward: A function to apply to the value before applying it to the target.

        Returns:
        - Self: The instance of the TextElement.

        """
        bind_to(self, 'text', target_object, target_name, forward)
        return self

    def bind_text_from(self,
                       target_object: Any,
                       target_name: str = 'text',
                       backward: Callable[..., Any] = lambda x: x,
                       ) -> Self:
        """
        Bind the text of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever a value changes.

        Args:
        - target_object: The object to bind from.
        - target_name: The name of the property to bind from.
        - backward: A function to apply to the value before applying it to this element.

        Returns:
        - Self: The instance of the TextElement.

        """
        bind_from(self, 'text', target_object, target_name, backward)
        return self

    def bind_text(self,
                  target_object: Any,
                  target_name: str = 'text', *,
                  forward: Callable[..., Any] = lambda x: x,
                  backward: Callable[..., Any] = lambda x: x,
                  ) -> Self:
        """
        Bind the text of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.
        The update happens immediately and whenever a value changes.
        The backward binding takes precedence for the initial synchronization.

        Args:
        - target_object: The object to bind to.
        - target_name: The name of the property to bind to.
        - forward: A function to apply to the value before applying it to the target.
        - backward: A function to apply to the value before applying it to this element.

        Returns:
        - Self: The instance of the TextElement.

        """
        bind(self, 'text', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_text(self, text: str) -> None:
            """
            Set the text of this element.

            Args:
                text (str): The new text to be set.

            Returns:
                None

            Raises:
                None

            Examples:
                >>> element = TextElement()
                >>> element.set_text("Hello, World!")
                >>> element.text
                'Hello, World!'

            This method sets the text of the element to the specified value. The text can be any string.
            After calling this method, the `text` attribute of the element will be updated with the new value.

            Note:
                This method does not perform any validation or formatting of the text. It simply assigns the
                provided value to the `text` attribute.

            """
            self.text = text

    def _handle_text_change(self, text: str) -> None:
        """
        Handles the change in text for the element.

        This method is responsible for updating the internal state of the element
        when the text is changed. It converts the provided `text` to the model's
        text format, updates the element, and triggers a re-rendering.

        Args:
            text (str): The new text for the element.

        Returns:
            None

        Example:
            >>> element = TextElement()
            >>> element._handle_text_change("Hello, world!")
            >>> element.get_text()
            'Hello, world!'
        """
        self._text_to_model_text(text)
        self.update()

    def _text_to_model_text(self, text: str) -> None:
        """
        Convert the text to model-specific text representation.

        This method is responsible for converting the given text into a format that is specific to the underlying model
        used by the text element. It updates the internal `_text` attribute with the converted text.

        Args:
            text (str): The text to convert.

        Returns:
            None

        Raises:
            Any exceptions that may occur during the conversion process.

        Example:
            >>> element = TextElement()
            >>> element._text_to_model_text("Hello, world!")
            >>> element._text
            'Hello, world!'

        Note:
            - This method should be called whenever the text needs to be updated in the model.
            - The specific implementation of this method may vary depending on the model used by the text element.

        See Also:
            - `TextElement`: The main class that uses this method.
        """
        self._text = text
