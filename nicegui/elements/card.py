from typing_extensions import Self

from ..element import Element


class Card(Element):

    def __init__(self) -> None:
        """Card

        This element is based on Quasar's `QCard <https://quasar.dev/vue-components/card>`_ component.
        It provides a container with a dropped shadow.

        Note:
        There are subtle differences between the Quasar component and this element.
        In contrast to this element, the original QCard has no padding by default and hides outer borders of nested elements.
        If you want the original behavior, use the `tight` method.
        If you want the padding and borders for nested children, move the children into another container.
        """
        super().__init__('q-card')
        self._classes.append('nicegui-card')

    def tight(self) -> Self:
        """Remove padding and gaps between nested elements."""
        return self.classes('nicegui-card-tight')


class CardSection(Element):

    def __init__(self) -> None:
        """Card Section

        This element is based on Quasar's `QCardSection <https://quasar.dev/vue-components/card#qcardsection-api>`_ component.
        """
        super().__init__('q-card-section')


class CardActions(Element):

    def __init__(self) -> None:
        """Card Actions

        This element is based on Quasar's `QCardActions <https://quasar.dev/vue-components/card#qcardactions-api>`_ component.
        """
        super().__init__('q-card-actions')
