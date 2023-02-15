from typing import Optional

from typing_extensions import Literal

from ..element import Element

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


class Spinner(Element):

    def __init__(self, type: Optional[SpinnerTypes] = 'default', *,
                 size: str = '1em', color: str = 'primary', thickness: float = 5.0):
        """Spinner

        See `Quasar Spinner <https://quasar.dev/vue-components/spinner>`_ for more information.

        :param type: type of spinner (e.g. "audio", "ball", "bars", ..., default: "default")
        :param size: size of the spinner (e.g. "3em", "10px", "xl", ..., default: "1em")
        :param color: color of the spinner (default: "primary")
        :param thickness: thickness of the spinner (applies to the "default" spinner only, default: 5.0)
        """
        super().__init__('q-spinner' if type == 'default' else f'q-spinner-{type}')
        self._props['size'] = size
        self._props['color'] = color
        self._props['thickness'] = thickness
