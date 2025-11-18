from __future__ import annotations

from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Rating(ValueElement, DisableableElement):

    def __init__(self,
                 value: float | None = None,
                 max: int = 5,  # pylint: disable=redefined-builtin
                 icon: str | None = None,
                 icon_selected: str | None = None,
                 icon_half: str | None = None,
                 color: str | list[str] | None = 'primary',
                 size: str | None = None,
                 on_change: Handler[ValueChangeEventArguments] | None = None,
                 ) -> None:
        """Rating

        This element is based on Quasar's `QRating <https://quasar.dev/vue-components/rating>`_ component.

        *Added in version 2.12.0*

        :param value: initial value (default: ``None``)
        :param max: maximum rating, number of icons (default: 5)
        :param icon: name of icons to be displayed (default: star)
        :param icon_selected: name of an icon to be displayed when selected (default: same as ``icon``)
        :param icon_half: name of an icon to be displayed when half-selected (default: same as ``icon``)
        :param color: color(s) of the icons (Quasar, Tailwind, or CSS colors or ``None``, default: "primary")
        :param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem
        :param on_change: callback to execute when selection changes
        """
        super().__init__(tag='q-rating', value=value, on_value_change=on_change)

        self._props['max'] = max

        if icon:
            self._props['icon'] = icon

        if color:
            self._props['color'] = color

        if icon_selected:
            self._props['icon-selected'] = icon_selected

        if icon_half:
            self._props['icon-half'] = icon_half

        if size:
            self._props['size'] = size
