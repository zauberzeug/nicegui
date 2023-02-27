from typing import Optional

from ..element import Element


class Avatar(Element):

    def __init__(self,
                 icon: str = 'none', *,
                 color: str = 'primary',
                 text_color: Optional[str] = None,
                 size: Optional[str] = None,
                 font_size: Optional[str] = None,
                 square: bool = False,
                 rounded: bool = False,
                 ) -> None:
        """Avatar

        A avatar element wrapping Quasar's
        `QAvatar <https://quasar.dev/vue-components/avatar>`_ component.

        :param icon: name of the icon or image path with "img:" prefix (e.g. "map", "img:path/to/image.png")
        :param color: color name for component from the Quasar Color Palette (e.g. "primary", "teal-10")
        :param text_color: color name from the Quasar Color Palette (e.g. "primary", "teal-10")
        :param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl) (e.g. "16px", "2rem")
        :param font_size: size in CSS units, including unit name, of the content (icon, text) (e.g. "18px", "2rem")
        :param square: removes border-radius so borders are squared (default: False)
        :param rounded: applies a small standard border-radius for a squared shape of the component (default: False)
        """
        super().__init__('q-avatar')

        self._props['icon'] = icon
        self._props['color'] = color
        self._props['square'] = square
        self._props['rounded'] = rounded

        if text_color is not None:
            self._props['text-color'] = text_color

        if size is not None:
            self._props['size'] = size

        if font_size is not None:
            self._props['font-size'] = font_size
