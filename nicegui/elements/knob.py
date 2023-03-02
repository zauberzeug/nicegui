from typing import Union

from ..dependencies import register_component
from .icon import Icon
from .label import Label
from .mixins.value_element import ValueElement


class Knob(ValueElement):

    def __init__(
        self,
        color: str = 'primary',
        center_color: str = 'white',
        track_color: str = 'secondary',
        size: str = '',
        show_value: Union[bool, None] = False,
        icon_name: Union[str, None] = None,
        icon_color: str = 'black',
        icon_size: str = '1rem',
    ) -> None:
        """Knob

        This element is based on Quasar's `QKnob <https://quasar.dev/vue-components/knob>`_ component.
        The element is used to take a number input from the user through mouse/touch panning.

        :param color: color name for component, examples: primary, teal-10.
        :param center_color: color name for the center part of the component, examples: primary, teal-10.
        :param track_color: color name for the track of the component, examples: primary, teal-10.
        :param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem.
        :param icon: name for the icon in the center of thecomponent, examples: volume_up, volume_down.
        :param icon_color: color name for the icon in the center of the component, examples: primary, teal-10.
        :param icon_size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem.
        """
        super().__init__(tag='q-knob', value=100, on_value_change=None)

        self._props['color'] = color
        self._props['center-color'] = center_color
        self._props['track-color'] = track_color
        self._props['size'] = size

        if show_value:
            self._props['show-value'] = True
            with self:
                Label('0').bind_text_from(self, 'value')

        if icon_name:
            self._props['show-value'] = True
            with self:
                self.icon = Icon(icon_name)
