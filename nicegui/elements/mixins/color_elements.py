from typing import Any, Optional

from ...element import Element

QUASAR_COLORS = {'primary', 'secondary', 'accent', 'dark', 'positive', 'negative', 'info', 'warning'}
for color in ['red', 'pink', 'purple', 'deep-purple', 'indigo', 'blue', 'light-blue', 'cyan', 'teal', 'green',
              'light-green', 'lime', 'yellow', 'amber', 'orange', 'deep-orange', 'brown', 'grey', 'blue-grey']:
    QUASAR_COLORS.add(color)
    for i in range(1, 15):
        QUASAR_COLORS.add(f'{color}-{i}')

TAILWIND_COLORS = {
    f'{name}-{value}'
    for name in ['red', 'orange', 'amber', 'yellow', 'lime', 'green', 'emerald', 'teal', 'cyan', 'sky', 'blue',
                 'indigo', 'violet', 'purple', 'fuchsia', 'pink', 'rose', 'slate', 'gray', 'zinc', 'neutral', 'stone']
    for value in [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]
}


class BackgroundColorElement(Element):
    BACKGROUND_COLOR_PROP = 'color'

    def __init__(self, *, background_color: Optional[str], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if background_color in QUASAR_COLORS:
            self._props[self.BACKGROUND_COLOR_PROP] = background_color
        elif background_color in TAILWIND_COLORS:
            self._classes.append(f'bg-{background_color}')
        elif background_color is not None:
            self._style['background-color'] = background_color


class TextColorElement(Element):
    TEXT_COLOR_PROP = 'color'

    def __init__(self, *, text_color: Optional[str], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if text_color in QUASAR_COLORS:
            self._props[self.TEXT_COLOR_PROP] = text_color
        elif text_color in TAILWIND_COLORS:
            self._classes.append(f'text-{text_color}')
        elif text_color is not None:
            self._style['color'] = text_color
