from .mixins.text_element import TextElement


class Badge(TextElement):

    def __init__(self, text: str = '', *,
                 color: str = 'blue', text_color: str = 'white', outline: bool = False) -> None:
        """Badge

        A badge element wrapping Quasar's
        `QBadge <https://quasar.dev/vue-components/badge>`_ component.

        :param text: the initial value of the text field
        :param color: the color name for component from the Quasar Color Palette (default: "blue")
        :param text_color: overrides text color (if needed); color name from the Quasar Color Palette (default: "white")
        :param outline: use 'outline' design (colored text and borders only) (default: False)
        """
        super().__init__(tag='q-badge', text=text)
        self._props['color'] = color
        self._props['text_color'] = text_color
        self._props['outline'] = outline
