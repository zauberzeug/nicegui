from ..element import Element


class Space(Element):

    def __init__(self) -> None:
        """Space

        This element is based on Quasar's `QSpace <https://quasar.dev/vue-components/space>`_ component.

        Its purpose is to simply fill all available space inside of a flexbox element.
        """
        super().__init__('q-space')
