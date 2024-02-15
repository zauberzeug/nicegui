from typing_extensions import Self

from ..element import Element


class Card(Element):
    """
    A container element with a dropped shadow, based on Quasar's QCard component.

    This element provides a container with a dropped shadow. It can be used to display
    various types of content, such as images, text, or other elements.

    Note:
    There are subtle differences between the Quasar component and this element.
    In contrast to this element, the original QCard has no padding by default and hides
    outer borders of nested elements. If you want the original behavior, use the `tight`
    method. If you want the padding and borders for nested children, move the children
    into another container.

    Usage:
    ```python
    card = Card()
    card.add_child(Text('Hello, world!'))
    card.add_child(Image('image.jpg'))
    ```
    """

    def __init__(self) -> None:
        """Card

        This element is based on Quasar's `QCard <https://quasar.dev/vue-components/card>`_ component.
        It provides a container with a dropped shadow.

        Note:
        There are subtle differences between the Quasar component and this element.
        In contrast to this element, the original QCard has no padding by default and hides
        outer borders of nested elements. If you want the original behavior, use the `tight`
        method. If you want the padding and borders for nested children, move the children
        into another container.
        """
        super().__init__('q-card')
        self._classes.append('nicegui-card')

    def tight(self) -> Self:
        """
        Remove padding and gaps between nested elements.

        Returns:
        Self: The Card instance with the 'nicegui-card-tight' class added.

        Usage:
        ```python
        card = Card()
        card.tight()
        ```
        """
        return self.classes('nicegui-card-tight')


class CardSection(Element):
    """Represents a section within a card.

    This element is based on Quasar's [QCardSection](https://quasar.dev/vue-components/card#qcardsection-api) component.

    Args:
        - Element (class): The base class for all elements.

    Attributes:
        tag (str): The HTML tag for the card section element.

    Example:
        Create a card section element:

        ```python
        section = CardSection()
        ```
    """
    def __init__(self) -> None:
        """
        Card Section

        This element is based on Quasar's [QCardSection](https://quasar.dev/vue-components/card#qcardsection-api) component.

        Args:
            None

        Returns:
            None
        """
        super().__init__('q-card-section')


class CardActions(Element):
    """Represents a set of actions for a card.

    This element is based on Quasar's [QCardActions](https://quasar.dev/vue-components/card#qcardactions-api) component.

    Args:
        - Element (class): The base class for all elements.

    Attributes:
        - tag (str): The HTML tag for the card actions element.

    Example:
        ```python
        actions = CardActions()
        ```
    """
    def __init__(self) -> None:
        """Initialize a Card Actions element.

        This element is based on Quasar's [QCardActions](https://quasar.dev/vue-components/card#qcardactions-api) component.

        Args:
            None

        Returns:
            None

        Example:
            >>> card_actions = CardActions()
        """
        super().__init__('q-card-actions')
