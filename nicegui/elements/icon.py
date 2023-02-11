from ..element import Element
from ..layout import IconLayout


class Icon(Element):

    def __init__(self, name: str) -> None:
        """Icon

        Displays an icon.

        `Here <https://material.io/icons/>`_ is a reference of possible names.

        :param name: the name of the icon
        """
        super().__init__('q-icon')
        self.layout = IconLayout(self)

        self._props['name'] = name
