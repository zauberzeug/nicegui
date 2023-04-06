from typing import Optional

from typing_extensions import get_args

from .element import Element
from .tailwind_types.background_color import BackgroundColor

QUASAR_COLORS = {'primary', 'secondary', 'accent', 'dark', 'positive', 'negative', 'info', 'warning'}
for color in {'red', 'pink', 'purple', 'deep-purple', 'indigo', 'blue', 'light-blue', 'cyan', 'teal', 'green',
              'light-green', 'lime', 'yellow', 'amber', 'orange', 'deep-orange', 'brown', 'grey', 'blue-grey'}:
    QUASAR_COLORS.add(color)
    for i in range(1, 15):
        QUASAR_COLORS.add(f'{color}-{i}')

TAILWIND_COLORS = get_args(BackgroundColor)


def set_text_color(element: Element, color: Optional[str], *, prop_name: str = 'color') -> None:
    if color in QUASAR_COLORS:
        element._props[prop_name] = color
    elif color in TAILWIND_COLORS:
        element._classes.append(f'text-{color}')
    elif color is not None:
        element._style['color'] = color


def set_background_color(element: Element, color: Optional[str], *, prop_name: str = 'color') -> None:
    if color in QUASAR_COLORS:
        element._props[prop_name] = color
    elif color in TAILWIND_COLORS:
        element._classes.append(f'bg-{color}')
    elif color is not None:
        element._style['background-color'] = color
