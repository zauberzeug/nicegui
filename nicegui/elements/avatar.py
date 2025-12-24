from typing import Optional

from ..defaults import DEFAULT_PROPS, resolve_defaults
from .mixins.color_elements import BackgroundColorElement, TextColorElement
from .mixins.icon_element import IconElement


class Avatar(IconElement, BackgroundColorElement, TextColorElement):
    TEXT_COLOR_PROP = 'text-color'

    @resolve_defaults
    def __init__(self,
                 icon: Optional[str] = None, *,
                 color: Optional[str] = DEFAULT_PROPS['color'] | 'primary',
                 text_color: Optional[str] = DEFAULT_PROPS['text-color'] | None,
                 size: Optional[str] = DEFAULT_PROPS['size'] | None,
                 font_size: Optional[str] = DEFAULT_PROPS['font-size'] | None,
                 square: bool = DEFAULT_PROPS['square'] | False,
                 rounded: bool = DEFAULT_PROPS['rounded'] | False,
                 ) -> None:
        """Avatar

        A avatar element wrapping Quasar's
        `QAvatar <https://quasar.dev/vue-components/avatar>`_ component.

        :param icon: name of the icon or image path with "img:" prefix (e.g. "map", "img:path/to/image.png")
        :param color: background color (either a Quasar, Tailwind, or CSS color or `None`, default: "primary")
        :param text_color: color name from the Quasar Color Palette (e.g. "primary", "teal-10")
        :param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl) (e.g. "16px", "2rem")
        :param font_size: size in CSS units, including unit name, of the content (icon, text) (e.g. "18px", "2rem")
        :param square: removes border-radius so borders are squared (default: False)
        :param rounded: applies a small standard border-radius for a squared shape of the component (default: False)
        """
        super().__init__(tag='q-avatar', background_color=color, text_color=text_color, icon=icon)

        self._props['square'] = square
        self._props['rounded'] = rounded
        self._props.set_optional('size', size)
        self._props.set_optional('font-size', font_size)
