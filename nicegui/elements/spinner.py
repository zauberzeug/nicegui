from typing import Literal

from ..defaults import DEFAULT_PROP, resolve_defaults
from .mixins.color_elements import TextColorElement

SpinnerTypes = Literal[
    'default',
    'audio',
    'ball',
    'bars',
    'box',
    'clock',
    'comment',
    'cube',
    'dots',
    'facebook',
    'gears',
    'grid',
    'hearts',
    'hourglass',
    'infinity',
    'ios',
    'orbit',
    'oval',
    'pie',
    'puff',
    'radio',
    'rings',
    'tail',
]


class Spinner(TextColorElement):

    @resolve_defaults
    def __init__(self,
                 type: SpinnerTypes | None = 'default', *,  # pylint: disable=redefined-builtin
                 size: str = DEFAULT_PROP | '1em',
                 color: str | None = DEFAULT_PROP | 'primary',
                 thickness: float = DEFAULT_PROP | 5.0,
                 ) -> None:
        """Spinner

        This element is based on Quasar's `QSpinner <https://quasar.dev/vue-components/spinners>`_ component.

        :param type: type of spinner (e.g. "audio", "ball", "bars", ..., default: "default")
        :param size: size of the spinner (e.g. "3em", "10px", "xl", ..., default: "1em")
        :param color: color of the spinner (either a Quasar, Tailwind, or CSS color or `None`, default: "primary")
        :param thickness: thickness of the spinner (applies to the "default" spinner only, default: 5.0)
        """
        super().__init__(tag='q-spinner' if type == 'default' else f'q-spinner-{type}', text_color=color)
        self._props['size'] = size
        self._props['thickness'] = thickness
