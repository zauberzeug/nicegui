from typing import Optional

from .mixins.color_elements import TextColorElement
from .mixins.name_element import NameElement


class Icon(NameElement, TextColorElement):
    """Represents an icon element.

    This element is based on Quasar's [QIcon](https://quasar.dev/vue-components/icon) component.

    Usage:
        icon = Icon(name, size=None, color=None)

    Args:
        - name (str): The name of the icon (snake case, e.g. `add_circle`).
        - size (Optional[str], optional): The size of the icon in CSS units, including unit name or standard size name (xs|sm|md|lg|xl). Examples: '16px', '2rem'. Defaults to None.
        - color (Optional[str], optional): The color of the icon (either a Quasar, Tailwind, or CSS color or `None`). Defaults to None.

    Attributes:
        - tag (str): The HTML tag for the icon element.
        - name (str): The name of the icon.
        - text_color (Optional[str]): The color of the icon's text.

    Note:
        - The `name` argument should be a valid icon name. You can refer to the [Material Icons](https://fonts.google.com/icons?icon.set=Material+Icons) reference for possible names.
        - The `size` argument is optional. If provided, it sets the size of the icon.
        - The `color` argument is optional. If provided, it sets the color of the icon.

    Example:
        # Create an icon element with name 'add_circle', size '16px', and color 'red'
        icon = Icon('add_circle', size='16px', color='red')
    """

    def __init__(self,
                 name: str,
                 *,
                 size: Optional[str] = None,
                 color: Optional[str] = None,
                 ) -> None:
        super().__init__(tag='q-icon', name=name, text_color=color)

        if size:
            self._props['size'] = size
