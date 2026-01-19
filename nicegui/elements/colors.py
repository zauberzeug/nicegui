from ..defaults import DEFAULT_PROP, resolve_defaults
from ..element import Element
from .mixins.color_elements import QUASAR_COLORS


class Colors(Element, component='colors.js'):

    @resolve_defaults
    def __init__(self, *,
                 primary: str = DEFAULT_PROP | '#5898d4',
                 secondary: str = DEFAULT_PROP | '#26a69a',
                 accent: str = DEFAULT_PROP | '#9c27b0',
                 dark: str = DEFAULT_PROP | '#1d1d1d',
                 dark_page: str = DEFAULT_PROP | '#121212',
                 positive: str = DEFAULT_PROP | '#21ba45',
                 negative: str = DEFAULT_PROP | '#c10015',
                 info: str = DEFAULT_PROP | '#31ccec',
                 warning: str = DEFAULT_PROP | '#f2c037',
                 **custom_colors: str) -> None:
        """Color Theming

        Sets the main colors (primary, secondary, accent, ...) used by `Quasar <https://quasar.dev/style/theme-builder>`_ on a per-page basis.

        Note: This takes precedence over the global color configuration set via ``app.colors()``.

        :param primary: Primary color (default: "#5898d4")
        :param secondary: Secondary color (default: "#26a69a")
        :param accent: Accent color (default: "#9c27b0")
        :param dark: Dark color (default: "#1d1d1d")
        :param dark_page: Dark page color (default: "#121212")
        :param positive: Positive color (default: "#21ba45")
        :param negative: Negative color (default: "#c10015")
        :param info: Info color (default: "#31ccec")
        :param warning: Warning color (default: "#f2c037")
        :param custom_colors: Custom color definitions for branding (needs ``ui.colors`` to be called before custom color is ever used, *added in version 2.2.0*)
        """
        super().__init__()
        self._props['primary'] = primary
        self._props['secondary'] = secondary
        self._props['accent'] = accent
        self._props['dark'] = dark
        self._props['dark-page'] = dark_page
        self._props['positive'] = positive
        self._props['negative'] = negative
        self._props['info'] = info
        self._props['warning'] = warning
        self._props['custom-colors'] = custom_colors
        QUASAR_COLORS.update({name.replace('_', '-') for name in custom_colors})

        self._props.add_rename('dark_page', 'dark-page')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('custom_colors', 'custom-colors')  # DEPRECATED: remove in NiceGUI 4.0
