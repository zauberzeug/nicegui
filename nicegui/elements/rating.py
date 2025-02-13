from typing import Optional, Union

from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Rating(ValueElement, DisableableElement):

    def __init__(self,
                 value: Optional[Union[int, float]] = None,
                 icon: Optional[str] = 'star',
                 icon_selected: Optional[str] = None,
                 color: Optional[str] = 'primary',
                 max: Optional[int] = 5, # pylint: disable=redefined-builtin
                 size: Optional[str] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """Rating

        This element is based on Quasar's `QRating <https://quasar.dev/vue-components/rating>`_ component.

        :param value: the initial value (default: `None`)
        :param icon: the name of an icon to be displayed (default: `star`)
        :param icon_selected: the name of an icon to be displayed when selected, if different (default: `None`)
        :param color: the color of the icon (either a Quasar, Tailwind, or CSS color or `None`, default: 'primary')
        :param max: the maximum number of rating icons displayed (default: `5`)
        :param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem
        :param on_change: callback to execute when selection changes
        """

        super().__init__(tag='q-rating', value=value, on_value_change=on_change, throttle=0.05)

        self._props['icon'] = icon
        self._props['color'] = color
        self._props['max'] = max

        if icon_selected:
            self._props['icon-selected'] = icon_selected

        if size:
            self._props['size'] = size
