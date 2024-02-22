from typing import Optional, Union

from .label import Label as label
from .mixins.color_elements import TextColorElement
from .mixins.value_element import ValueElement


class LinearProgress(ValueElement, TextColorElement):
    VALUE_PROP = "value"

    def __init__(
        self,
        value: float = 0.0,
        *,
        min: float = 0.0,  # pylint: disable=redefined-builtin
        max: Optional[Union[str, int]] = 1.0,  # pylint: disable=redefined-builtin
        size: Optional[Union[str, int]] = None,
        show_value: bool = True,
        color: Optional[str] = "primary",
        reverse: bool = False,
        buffer: Optional[float] = None,
        track_color=None,
        dark: bool = False,
        rounded: bool = False,
        animation_speed: int = 2100,
        indeterminate: bool = False,
        query: bool = False,
        instant_feedback: bool = False,
        stripe: bool = False,
    ) -> None:
        """Linear Progress

        A linear progress bar wrapping Quasar's
        `QLinearProgress <https://quasar.dev/vue-components/linear-progress>`_ component.

        :param value: the initial value of the field (from 0.0 to 1.0)
        :param size: the height of the progress bar (default: "20px" with value label and "4px" without)
        :param show_value: whether to show a value label in the center (default: `True`)
        :param color: color (either a Quasar, Tailwind, or CSS color or `None`, default: "primary")
        """
        if max > 1.0:
            value = float(value / max)

        super().__init__(
            tag="q-linear-progress",
            value=value,
            on_value_change=None,
            text_color=color,
        )
        self._props["min"] = min
        self._props["max"] = max

        if isinstance(size, int):
            size = str(size) + "px"
        self._props["size"] = size

        self._props["reverse"] = reverse
        self._props["buffer"] = buffer / max if buffer else None

        self._props[
            "show-value"
        ] = True  # NOTE always activate the default slot because this is expected by ui.element

        self._props["track-color"] = track_color
        self._props["dark"] = dark
        self._props["rounded"] = rounded
        self._props["animation-speed"] = animation_speed
        self._props["indeterminate"] = indeterminate
        self._props["query"] = query
        self._props["instant-feedback"] = instant_feedback
        self._props["stripe"] = stripe

        if show_value:
            with self:
                label().classes("absolute-center text-sm text-white").bind_text_from(
                    self,
                    "value",
                    backward=lambda v=value: int(v * max).__round__(0)
                    if max > 1.0
                    else float(v * max),
                )


class CircularProgress(ValueElement, TextColorElement):
    VALUE_PROP = "value"

    def __init__(
        self,
        value: float = 0.0,
        *,
        min: float = 0.0,  # pylint: disable=redefined-builtin
        max: float = 1.0,  # pylint: disable=redefined-builtin
        size: Optional[Union[str, int]] = "xl",
        font_size: Optional[Union[str, int]] = "0.25em",
        show_value: bool = True,
        angle: int = 0,
        color: Optional[str] = "primary",
        center_color: Optional[str] = None,
        track_color: Optional[str] = "grey-4",
        indeterminate: bool = False,
        reverse: bool = False,
        instant_feedback: bool = False,
        rounded: bool = False,
        thickness: Optional[Union[float, int]] = 0.2,
        animation_speed: int = 600,
    ) -> None:
        """Circular Progress

        A circular progress bar wrapping Quasar's
        `QCircularProgress <https://quasar.dev/vue-components/circular-progress>`_.

        :param value: the initial value of the field
        :param min: the minimum value (default: 0.0)
        :param max: the maximum value (default: 1.0)
        :param size: the size of the progress circle (default: "xl")
        :param show_value: whether to show a value label in the center (default: `True`)
        :param color: color (either a Quasar, Tailwind, or CSS color or `None`, default: "primary")
        """
        super().__init__(
            tag="q-circular-progress",
            value=value,
            on_value_change=None,
            text_color=color,
        )
        self._props["min"] = min
        self._props["max"] = max

        if isinstance(size, int):
            size = str(size) + "px"
        self._props["size"] = size

        if isinstance(font_size, int):
            font_size = str(font_size) + "px"
        self._props["font_size"] = font_size

        self._props["angle"] = angle

        self._props[
            "show-value"
        ] = True  # NOTE always activate the default slot because this is expected by ui.element

        self._props["track-color"] = track_color
        self._props["center-color"] = center_color
        self._props["indeterminate"] = indeterminate
        self._props["reverse"] = reverse
        self._props["instant-feedback"] = instant_feedback
        self._props["rounded"] = rounded
        self._props["thickness"] = thickness
        self._props["animation-speed"] = animation_speed

        if show_value:
            with self:
                label().classes("absolute-center text-xs").bind_text_from(self, "value")
