from .mixins.text_element import TextElement


class Tooltip(TextElement):

    def __init__(self, text: str) -> None:
        """Tooltip

        This element is based on Quasar's `QTooltip <https://quasar.dev/vue-components/tooltip>`_ component.
        It be placed in another element to show additional information on hover.

        :param text: the content of the tooltip
        """
        super().__init__(tag='q-tooltip', text=text)
