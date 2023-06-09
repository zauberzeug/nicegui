from typing import Optional

from ..colors import set_text_color
from ..element import Element


class Icon(Element):

    def __init__(self,
                 name: str,
                 *,
                 size: Optional[str] = None,
                 color: Optional[str] = None,
                 ) -> None:
        """Icon

        This element is based on Quasar's [QIcon](https://quasar.dev/vue-components/icon>) component.

        [Here](https://material.io/icons/>) is a reference of possible names.

        ### Parameters
        - `name`: name of the icon
        - `size`: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem
        - `color`: icon color (either a Quasar, Tailwind, or CSS color or `None`, default: `None`)
        """
        super().__init__('q-icon')
        self._props['name'] = name

        if size:
            self._props['size'] = size

        set_text_color(self, color)
