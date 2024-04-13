from ..element import Element


class List(Element):

    def __init__(self) -> None:
        """List

        A list element based on Quasar's `QList <https://quasar.dev/vue-components/list-and-list-items#qlist-api>`_ component.
        It provides a container for ``ui.item`` elements.
        """
        super().__init__('q-list')
