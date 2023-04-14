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
        self._classes = ['nicegui-card']

    def tight(self):
        """Removes padding and gaps between nested elements."""
        self._classes.clear()
        self._style.clear()
        return self


class CardSection(Element):

    def __init__(self) -> None:
        super().__init__('q-card-section')


class CardActions(Element):

    def __init__(self) -> None:
        super().__init__('q-card-actions')
