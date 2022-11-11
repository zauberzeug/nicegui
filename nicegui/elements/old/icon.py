import justpy as jp

from .element import Element


class Icon(Element):

    def __init__(self, name: str):
        """Icon

        Displays an icon.

        `Here <https://material.io/icons/>`_ is a reference of possible names.

        :param name: the name of the icon
        """
        view = jp.QIcon(name=name, classes=f'q-pt-xs', size='20px', temp=False)

        super().__init__(view)
