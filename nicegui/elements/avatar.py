from typing import Optional

from .mixins.color_elements import BackgroundColorElement, TextColorElement


class Avatar(BackgroundColorElement, TextColorElement):
    """Avatar

    This class represents an Avatar element, which is a wrapper around Quasar's QAvatar component.
    It allows you to create avatars with customizable properties such as icon, background color,
    text color, size, font size, and shape.

    Args:
        - icon (Optional[str]): The name of the icon or image path with "img:" prefix (e.g. "map", "img:path/to/image.png").
        - color (Optional[str]): The background color of the avatar. It can be a Quasar, Tailwind, or CSS color, or `None` for the default color ("primary").
        - text_color (Optional[str]): The color name from the Quasar Color Palette for the text content of the avatar (e.g. "primary", "teal-10").
        - size (Optional[str]): The size of the avatar in CSS units, including the unit name or standard size name (xs|sm|md|lg|xl) (e.g. "16px", "2rem").
        - font_size (Optional[str]): The size of the content (icon, text) in CSS units, including the unit name (e.g. "18px", "2rem").
        - square (bool): If True, removes the border-radius so the borders are squared. Default is False.
        - rounded (bool): If True, applies a small standard border-radius for a squared shape of the component. Default is False.

    See Also:
        - [QAvatar Component Documentation](https://quasar.dev/vue-components/avatar)
    """
    TEXT_COLOR_PROP = 'text-color'

    def __init__(self,
                 icon: Optional[str] = None, *,
                 color: Optional[str] = 'primary',
                 text_color: Optional[str] = None,
                 size: Optional[str] = None,
                 font_size: Optional[str] = None,
                 square: bool = False,
                 rounded: bool = False,
                 ) -> None:
        """Avatar
        
        A avatar element wrapping Quasar's
        [QAvatar ](https://quasar.dev/vue-components/avatar) component.

        Args:
        
            - icon (Optional[str]): The name of the icon or image path with "img:" prefix.
            - color (Optional[str]): The background color of the avatar.
            - text_color (Optional[str]): The color name for the text content of the avatar.
            - size (Optional[str]): The size of the avatar in CSS units.
            - font_size (Optional[str]): The size of the content (icon, text) in CSS units.
            - square (bool): If True, removes the border-radius so the borders are squared.
            - rounded (bool): If True, applies a small standard border-radius for a squared shape of the component.
        """
        super().__init__(tag='q-avatar', background_color=color, text_color=text_color)

        if icon is not None:
            self._props['icon'] = icon
        self._props['square'] = square
        self._props['rounded'] = rounded

        if size is not None:
            self._props['size'] = size

        if font_size is not None:
            self._props['font-size'] = font_size
