from ..dependencies import register_component
from ..element import Element

register_component('colors', __file__, 'colors.js')


class Colors(Element):

    def __init__(self, *,
                 primary='#5898d4',
                 secondary='#26a69a',
                 accent='#9c27b0',
                 positive='#21ba45',
                 negative='#c10015',
                 info='#31ccec',
                 warning='#f2c037') -> None:
        """Color Theming

        Sets the main colors (primary, secondary, accent, ...) used by `Quasar <https://quasar.dev/>`_.
        """
        super().__init__('colors')
        self.looks._props['primary'] = primary
        self.looks._props['secondary'] = secondary
        self.looks._props['accent'] = accent
        self.looks._props['positive'] = positive
        self.looks._props['negative'] = negative
        self.looks._props['info'] = info
        self.looks._props['warning'] = warning
        self.update()
