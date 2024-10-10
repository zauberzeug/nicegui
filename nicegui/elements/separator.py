from ..element import Element


class Separator(Element, default_classes='nicegui-separator'):

    def __init__(self) -> None:
        """Separator

        This element is based on Quasar's `QSeparator <https://quasar.dev/vue-components/separator>`_ component.

        It serves as a separator for cards, menus and other component containers and is similar to HTML's <hr> tag.
        """
        super().__init__('q-separator')
