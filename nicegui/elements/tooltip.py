from .mixins.text_element import TextElement


class Tooltip(TextElement):

    def __init__(self, text: str = '') -> None:
        """Tooltip

        This element is based on Quasar's `QTooltip <https://quasar.dev/vue-components/tooltip>`_ component.
        It can be placed in another element to show additional information on hover.

        Instead of passing a string as the first argument, you can also nest other elements inside the tooltip.

        :param text: the content of the tooltip (default: '')
        """
        super().__init__(tag='q-tooltip', text=text)
