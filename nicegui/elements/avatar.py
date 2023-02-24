from typing import Literal

from ..element import Element


class Avatar(Element):
    def __init__(self, icon: str = "", color: str = "primary", text_color: str | None = None, size: str | None = None,
                 font_size: str | None = None, shape: Literal['roundend', 'square'] | None = None) -> None:
        """Avatar

        A avatar element wrapping Quasar's
        `QAvatar <https://quasar.dev/vue-components/avatar>`_ component.

        :param icon: the name of the icon or icon path (img:path/to/some_image.png)
        :param color: color name for component from the Quasar Color Palette, examples: primary, teal-10.
        :param text_color: color name from the Quasar Color Palette, examples: primary, teal-10.
        :param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem.
        :param font_size: size in CSS units, including unit name, of the content (icon, text), examples: 18px, 2rem.
        :param shape: shape of the avatar, examples: roundend, square.
        """
        super().__init__("q-avatar")

        self._props["icon"] = icon
        self._props["color"] = color

        if text_color is not None:
            self._props["text-color"] = text_color

        if size is not None:
            self._props["size"] = size

        if font_size is not None:
            self._props["font-size"] = font_size

        if shape is not None:
            self._props[shape] = True
