from ..element import Element


class Colors(Element, component='colors.js'):
    """A class representing color theming for NiceGUI elements.

    The `Colors` class sets the main colors used by NiceGUI elements, based on the [Quasar](https://quasar.dev/) framework.

    Attributes:
        primary (str): The primary color.
        secondary (str): The secondary color.
        accent (str): The accent color.
        dark (str): The dark color.
        positive (str): The positive color.
        negative (str): The negative color.
        info (str): The info color.
        warning (str): The warning color.

    Example:
        colors = Colors(primary='#5898d4', secondary='#26a69a', accent='#9c27b0')
        colors.update()
    """

    def __init__(self, *,
                 primary='#5898d4',
                 secondary='#26a69a',
                 accent='#9c27b0',
                 dark='#1d1d1d',
                 positive='#21ba45',
                 negative='#c10015',
                 info='#31ccec',
                 warning='#f2c037') -> None:
        """Initialize the Colors object with the specified color values.

        Args:
            primary (str, optional): The primary color. Defaults to '#5898d4'.
            secondary (str, optional): The secondary color. Defaults to '#26a69a'.
            accent (str, optional): The accent color. Defaults to '#9c27b0'.
            dark (str, optional): The dark color. Defaults to '#1d1d1d'.
            positive (str, optional): The positive color. Defaults to '#21ba45'.
            negative (str, optional): The negative color. Defaults to '#c10015'.
            info (str, optional): The info color. Defaults to '#31ccec'.
            warning (str, optional): The warning color. Defaults to '#f2c037'.
        """
        super().__init__()
        self._props['primary'] = primary
        self._props['secondary'] = secondary
        self._props['accent'] = accent
        self._props['dark'] = dark
        self._props['positive'] = positive
        self._props['negative'] = negative
        self._props['info'] = info
        self._props['warning'] = warning
        self.update()
