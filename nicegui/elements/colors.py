from ..element import Element


class Colors(Element, component='colors.js'):

    def __init__(self, *,
                 primary: str = '#5898d4',
                 secondary: str = '#26a69a',
                 accent: str = '#9c27b0',
                 dark: str = '#1d1d1d',
                 dark_page: str = '#121212',
                 positive: str = '#21ba45',
                 negative: str = '#c10015',
                 info: str = '#31ccec',
                 warning: str = '#f2c037') -> None:
        """Color Theming

        Sets the main colors (primary, secondary, accent, ...) used by `Quasar <https://quasar.dev/style/theme-builder>`_.

        :param primary: Primary color (default: "#5898d4")
        :param secondary: Secondary color (default: "#26a69a")
        :param accent: Accent color (default: "#9c27b0")
        :param dark: Dark color (default: "#1d1d1d")
        :param dark_page: Dark page color (default: "#121212")
        :param positive: Positive color (default: "#21ba45")
        :param negative: Negative color (default: "#c10015")
        :param info: Info color (default: "#31ccec")
        :param warning: Warning color (default: "#f2c037")
        """
        super().__init__()
        self._props['primary'] = primary
        self._props['secondary'] = secondary
        self._props['accent'] = accent
        self._props['dark'] = dark
        self._props['dark_page'] = dark_page
        self._props['positive'] = positive
        self._props['negative'] = negative
        self._props['info'] = info
        self._props['warning'] = warning
        self.update()
