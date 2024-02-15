from typing import Optional

from .mixins.color_elements import BackgroundColorElement, TextColorElement
from .mixins.text_element import TextElement


class Badge(TextElement, BackgroundColorElement, TextColorElement):
    """A badge element wrapping Quasar's QBadge component.

    Args:
        - text (str): The initial value of the text field.
        - color (Optional[str]): The color name for the component (either a Quasar, Tailwind, or CSS color or `None`). Default is "primary".
        - text_color (Optional[str]): The text color (either a Quasar, Tailwind, or CSS color or `None`). Default is `None`.
        - outline (bool): Use 'outline' design (colored text and borders only). Default is False.

    Attributes:
        TEXT_COLOR_PROP (str): The property name for text color.

    Note:
        This class inherits from TextElement, BackgroundColorElement, and TextColorElement.

    Examples:
        Create a badge with default settings:
        ```python
        badge = Badge()
        ```

        Create a badge with custom text and color:
        ```python
        badge = Badge(text='New', color='secondary')
        ```

        Create an outlined badge:
        ```python
        badge = Badge(outline=True)
        ```

    """

    TEXT_COLOR_PROP = 'text-color'

    def __init__(self,
                     text: str = '', *,
                     color: Optional[str] = 'primary',
                     text_color: Optional[str] = None,
                     outline: bool = False) -> None:
            """Badge
            A badge element wrapping Quasar's
            [QBadge ](https://quasar.dev/vue-components/badge) component.
            
            Args:
            
                - text (str): The initial value of the text field.
                - color (Optional[str]): The color name for the component (either a Quasar, Tailwind, or CSS color or `None`). Default is "primary".
                - text_color (Optional[str]): The text color (either a Quasar, Tailwind, or CSS color or `None`). Default is `None`.
                - outline (bool): Use 'outline' design (colored text and borders only). Default is False.

            Raises:
                None

            Returns:
                None
                
            Note:
            
                The Badge class represents a badge component that can be used to display a small piece of information, such as a notification count or a status indicator.
                The `text` parameter sets the initial value of the text field in the badge.
                The `color` parameter specifies the color of the badge. It can be either a Quasar, Tailwind, or CSS color name, or `None` for the default color.
                The `text_color` parameter sets the color of the text in the badge. It can be either a Quasar, Tailwind, or CSS color name, or `None` for the default text color.
                The `outline` parameter determines whether the badge should have an 'outline' design, which means it will have colored text and borders only.

                ```

            """
            super().__init__(tag='q-badge', text=text, text_color=text_color, background_color=color)
            self._props['outline'] = outline
