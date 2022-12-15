from .mixins.text_element import TextElement


class Tooltip(TextElement):

    def __init__(self, text: str) -> None:
        """Tooltip

        Can be placed in another element to show additional information on hover.

        :param text: the content of the tooltip
        """
        super().__init__(tag='q-tooltip', text=text)
