from typing import Any, Optional, get_args

from ...element import Element
from ...tailwind_types.background_color import BackgroundColor

QUASAR_COLORS = {'primary', 'secondary', 'accent', 'dark', 'positive', 'negative', 'info', 'warning'}
for color in ['red', 'pink', 'purple', 'deep-purple', 'indigo', 'blue', 'light-blue', 'cyan', 'teal', 'green',
              'light-green', 'lime', 'yellow', 'amber', 'orange', 'deep-orange', 'brown', 'grey', 'blue-grey']:
    QUASAR_COLORS.add(color)
    for i in range(1, 15):
        QUASAR_COLORS.add(f'{color}-{i}')

TAILWIND_COLORS = get_args(BackgroundColor)


class BackgroundColorElement(Element):
    """
    Represents an element with a background color.

    This class provides a way to set the background color of an element in a GUI application.
    It supports various color formats, including Quasar colors, Tailwind CSS colors, and custom color values.

    Args:
        - background_color (Optional[str]): The background color to be set. It can be a Quasar color name,
            a Tailwind CSS color name, or a custom color value. Defaults to None.

    Other Parameters:
        - **kwargs: Additional keyword arguments to be passed to the base class constructor.

    Attributes:
        - BACKGROUND_COLOR_PROP (str): The property name for the background color.

    Usage:
        To create an element with a background color, instantiate the BackgroundColorElement class
        and pass the desired background_color as a keyword argument.

        Example:
            element = BackgroundColorElement(background_color='red')

    Note:
        - Quasar colors: https://quasar.dev/style/color-palette
        - Tailwind CSS colors: https://tailwindcss.com/docs/customizing-colors#color-palette-reference
    """

    BACKGROUND_COLOR_PROP = 'color'

    def __init__(self, *, background_color: Optional[str], **kwargs: Any) -> None:
        """
        Initialize the ColorMixin class.

        Args:
           - background_color (Optional[str]): The background color of the element.
                It can be a Quasar color name, a Tailwind CSS color name, or a valid CSS color value.
                If a Quasar color name is provided, it will be set as the background color property.
                If a Tailwind CSS color name is provided, it will be added as a background class.
                If a valid CSS color value is provided, it will be set as the background color style.
            **kwargs (Any): Additional keyword arguments to be passed to the parent class.

        Returns:
           - None

        Raises:
           - None

        Examples:
            # Set background color using Quasar color name
            element = ColorMixin(background_color='primary')

            # Set background color using Tailwind CSS color name
            element = ColorMixin(background_color='red')

            # Set background color using CSS color value
            element = ColorMixin(background_color='#ff0000')
        """
        super().__init__(**kwargs)
        if background_color in QUASAR_COLORS:
            self._props[self.BACKGROUND_COLOR_PROP] = background_color
        elif background_color in TAILWIND_COLORS:
            self._classes.append(f'bg-{background_color}')
        elif background_color is not None:
            self._style['background-color'] = background_color


class TextColorElement(Element):
    """
    A mixin class for elements that have text color properties.

    This mixin provides functionality to set the text color of an element.
    It supports Quasar colors, Tailwind colors, and custom color values.

    Attributes:
        - TEXT_COLOR_PROP (str): The property name for the text color.

    Args:
        - text_color (Optional[str]): The text color to be set. It can be a Quasar color,
            a Tailwind color, or a custom color value. Defaults to None.

    Example:
        To create an element with a specific text color:

        ```python
        element = TextColorElement(text_color='red')
        ```

    Note:
        - Quasar colors: [Quasar Colors](https://quasar.dev/style/color-palette)
        - Tailwind colors: [Tailwind CSS Colors](https://tailwindcss.com/docs/customizing-colors)
    """

    TEXT_COLOR_PROP = 'color'

    def __init__(self, *, text_color: Optional[str], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if text_color in QUASAR_COLORS:
            self._props[self.TEXT_COLOR_PROP] = text_color
        elif text_color in TAILWIND_COLORS:
            self._classes.append(f'text-{text_color}')
        elif text_color is not None:
            self._style['color'] = text_color
