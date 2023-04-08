from typing import Optional

from ..colors import set_background_color, set_text_color
from .mixins.text_element import TextElement


class Badge(TextElement):

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
        super().__init__(tag='q-badge', text=text)
        set_background_color(self, color)
        set_text_color(self, text_color, prop_name='text-color')
        self._props['outline'] = outline
