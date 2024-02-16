from typing import Any, Callable, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class ContentElement(Element):
    """
    Represents an element that contains content.

    This class provides methods for binding and setting the content of the element.
    The content can be bound to another object's property, allowing for automatic updates.
    """

    CONTENT_PROP = 'innerHTML'
    content = BindableProperty(
        on_change=lambda sender, content: cast(Self, sender)._handle_content_change(content))  # pylint: disable=protected-access

    def __init__(self, *, content: str, **kwargs: Any) -> None:
        """
        Initializes a new instance of the ContentElement class.

        Args:
            - content: The initial content of the element.
            - **kwargs: Additional keyword arguments to pass to the base class constructor.
        """
        super().__init__(**kwargs)
        self.content = content
        self._handle_content_change(content)

    def bind_content_to(self,
                        target_object: Any,
                        target_name: str = 'content',
                        forward: Callable[..., Any] = lambda x: x,
                        ) -> Self:
        """
        Binds the content of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever a value changes.

        Args:
            - target_object: The object to bind to.
            - target_name: The name of the property to bind to.
            - forward: A function to apply to the value before applying it to the target.

        Returns:
            - The current instance of the ContentElement class.
        """
        bind_to(self, 'content', target_object, target_name, forward)
        return self

    def bind_content_from(self,
                          target_object: Any,
                          target_name: str = 'content',
                          backward: Callable[..., Any] = lambda x: x,
                          ) -> Self:
        """
        Binds the content of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever a value changes.

        Args:
            - target_object: The object to bind from.
            - target_name: The name of the property to bind from.
            - backward: A function to apply to the value before applying it to this element.

        Returns:
            - The current instance of the ContentElement class.
        """
        bind_from(self, 'content', target_object, target_name, backward)
        return self

    def bind_content(self,
                     target_object: Any,
                     target_name: str = 'content', *,
                     forward: Callable[..., Any] = lambda x: x,
                     backward: Callable[..., Any] = lambda x: x,
                     ) -> Self:
        """
        Binds the content of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.
        The update happens immediately and whenever a value changes.
        The backward binding takes precedence for the initial synchronization.

        Args:
            - target_object: The object to bind to.
            - target_name: The name of the property to bind to.
            - forward: A function to apply to the value before applying it to the target.
            - backward: A function to apply to the value before applying it to this element.

        Returns:
            - The current instance of the ContentElement class.
        """
        bind(self, 'content', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_content(self, content: str) -> None:
        """
        Sets the content of this element.

        Args:
            - content: The new content.
        """
        self.content = content

    def _handle_content_change(self, content: str) -> None:
        """
        Called when the content of this element changes.

        Args:
            - content: The new content.

        Raises:
            - ValueError: If the content contains a <script> tag.
        """
        if self.CONTENT_PROP == 'innerHTML' and '</script>' in content:
            raise ValueError('HTML elements must not contain <script> tags. Use ui.add_body_html() instead.')
        self._props[self.CONTENT_PROP] = content
        self.update()
