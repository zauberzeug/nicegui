from ..element import Element


class Card(Element):

    def __init__(self) -> None:
        """Card

        Provides a container with a dropped shadow.
        """
        super().__init__('q-card')
        self._classes = ['nicegui-card']

    def tight(self):
        self._classes.clear()
        self._style.clear()
        return self


class CardSection(Element):

    def __init__(self) -> None:
        super().__init__('q-card-section')


class CardActions(Element):

    def __init__(self) -> None:
        super().__init__('q-card-actions')
