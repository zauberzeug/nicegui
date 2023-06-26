from typing import Optional

from .mixins.color_elements import BackgroundColorElement, TextColorElement
from .mixins.text_element import TextElement


class Badge(TextElement, BackgroundColorElement, TextColorElement):
    TEXT_COLOR_PROP = 'text-color'

    def __init__(self,
                 text: str = '', *,
                 color: Optional[str] = 'primary',
                 text_color: Optional[str] = None,
                 outline: bool = False) -> None:
        """Badge

        A badge element wrapping Quasar's
        `QBadge <https://quasar.dev/vue-components/badge>`_ component.

        :param text: the initial value of the text field
        :param color: the color name for component (either a Quasar, Tailwind, or CSS color or `None`, default: "primary")
        :param text_color: text color (either a Quasar, Tailwind, or CSS color or `None`, default: `None`)
        :param outline: use 'outline' design (colored text and borders only) (default: False)
        """
        super().__init__(tag='q-badge', text=text, text_color=text_color, background_color=color)
        self._props['outline'] = outline
