from typing import Callable, Optional, get_args

from ..events import ClickEventArguments, handle_event
from ..tailwind_types.background_color import BackgroundColor
from .mixins.text_element import TextElement

QUASAR_COLORS = {'primary', 'secondary', 'accent', 'dark', 'positive', 'negative', 'info', 'warning'}
for color in {'red', 'pink', 'purple', 'deep-purple', 'indigo', 'blue', 'light-blue', 'cyan', 'teal', 'green',
              'light-green', 'lime', 'yellow', 'amber', 'orange', 'deep-orange', 'brown', 'grey', 'blue-grey'}:
    for i in range(1, 15):
        QUASAR_COLORS.add(f'{color}-{i}')

TAILWIND_COLORS = get_args(BackgroundColor)


class Button(TextElement):

    def __init__(self,
                 text: str = '', *,
                 on_click: Optional[Callable] = None,
                 color: Optional[str] = 'primary') -> None:
        """Button

        This element is based on Quasar's `QBtn <https://quasar.dev/vue-components/button>`_ component.

        The ``color`` parameter excepts a Quasar color, a Tailwind color, or a CSS color.
        If a Quasar color is used, the button will be styled according to the Quasar theme including the color of the text.
        Note that there are colors like "red" being both a Quasar color and a CSS color.
        In such cases the Quasar color will be used.

        :param text: the label of the button
        :param on_click: callback which is invoked when button is pressed
        :param color: the color of the button (either a Quasar, Tailwind, or CSS color or `None`, default: 'primary')
        """
        super().__init__(tag='q-btn', text=text)
        if color in QUASAR_COLORS:
            self._props['color'] = color
        elif color in TAILWIND_COLORS:
            self._classes.append(f'bg-{color}')
        elif color is not None:
            self._style['background-color'] = color

        if on_click:
            self.on('click', lambda _: handle_event(on_click, ClickEventArguments(sender=self, client=self.client)))

    def _text_to_model_text(self, text: str) -> None:
        self._props['label'] = text
