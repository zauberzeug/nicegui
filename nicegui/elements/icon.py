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
        orig = self.layout
        self.layout = IconLayout(self)
        self.layout._classes = orig._classes
        self.layout._props = orig._props

        self.layout._props['name'] = name
