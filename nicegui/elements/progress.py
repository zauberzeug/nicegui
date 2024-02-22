from typing import Optional, Union

from .label import Label as label
from .mixins.color_elements import TextColorElement
from .mixins.value_element import ValueElement


class LinearProgress(ValueElement, TextColorElement):
    VALUE_PROP = 'value'

    def __init__(
        self,
        value: float = 0.0,
        *,
        min: float = 0.0,  # pylint: disable=redefined-builtin
        max: Union[float, int] = 1.0,  # pylint: disable=redefined-builtin
        size: Union[str, int] = 20,
        show_value: bool = True,
        color: str = "primary",
        reverse: bool = False,
        buffer: Optional[float] = None,
        track_color=None,
        text_color: str = "white",
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
        It provides a way to display a progress bar with customizable options.

        :param value: The initial value of the progress bar (from 0.0 to 1.0).
        :param min: The minimum value of the progress bar (default: 0.0).
        :param max: The maximum value of the progress bar (default: 1.0).
        :param size: The height of the progress bar (default: None).
        :param show_value: Whether to show a value label in the center (default: True).
        :param color: The color of the progress bar (either a Quasar, Tailwind, or CSS color or `None`, default: "primary").
        :param reverse: Whether to reverse the direction of the progress bar (default: False).
        :param buffer: The buffer value of the progress bar (default: None).
        :param track_color: The color of the progress bar track (either a Quasar, Tailwind, or CSS color or `None`, default: None).
        :param dark: Whether to use dark mode for the progress bar (default: False).
        :param rounded: Whether to use rounded corners for the progress bar (default: False).
        :param animation_speed: The animation speed of the progress bar (default: 2100).
        :param indeterminate: Whether the progress bar is indeterminate (default: False).
        :param query: Whether the progress bar is in query mode (default: False).
        :param instant_feedback: Whether to provide instant feedback for the progress bar (default: False).
        :param stripe: Whether to show a stripe pattern on the progress bar (default: False).
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
                ).tailwind.text_color(text_color)


class CircularProgress(ValueElement, TextColorElement):
    VALUE_PROP = "value"

    def __init__(
        self,
        value: float = 0.0,
        *,
        min: float = 0.0,  # pylint: disable=redefined-builtin
        max: Union[float, int],  # pylint: disable=redefined-builtin
        size: Union[str, int] = "xl",
        font_size: Union[str, int] = "0.25em",
        show_value: bool = True,
        angle: int = 0,
        color: str = "primary",
        center_color: str = "transparent",
        track_color: str = "grey-4",
        text_color: str = "white",
        indeterminate: bool = False,
        reverse: bool = False,
        instant_feedback: bool = False,
        rounded: bool = False,
        thickness: Union[float, int] = 0.2,
        animation_speed: int = 600,
    ) -> None:
        """Circular Progress

        A circular progress bar wrapping Quasar's
        `QCircularProgress <https://quasar.dev/vue-components/circular-progress>`_.

        :param value: the initial value of the field
        :param min: the minimum value (default: 0.0)
        :param max: the maximum value (default: 1.0)
        :param size: the size of the progress circle (default: "xl")
        :param font_size: the font size of the value label (default: "0.25em")
        :param show_value: whether to show a value label in the center (default: `True`)
        :param angle: the starting angle of the progress circle (default: 0)
        :param color: the color of the progress circle (either a Quasar, Tailwind, or CSS color or `None`, default: "primary")
        :param center_color: the color of the center circle (either a Quasar, Tailwind, or CSS color or `None`, default: None)
        :param track_color: the color of the track circle (either a Quasar, Tailwind, or CSS color or `None`, default: "grey-4")
        :param indeterminate: whether the progress is indeterminate (default: False)
        :param reverse: whether the progress is reversed (default: False)
        :param instant_feedback: whether to provide instant feedback on value change (default: False)
        :param rounded: whether to use rounded edges for the progress circle (default: False)
        :param thickness: the thickness of the progress circle (default: 0.2)
        :param animation_speed: the speed of the progress animation in milliseconds (default: 600)
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
        self._props["text-color"] = text_color
        self._props["center-color"] = center_color
        self._props["indeterminate"] = indeterminate
        self._props["reverse"] = reverse
        self._props["instant-feedback"] = instant_feedback
        self._props["rounded"] = rounded
        self._props["thickness"] = thickness
        self._props["animation-speed"] = animation_speed

        if show_value:
            with self:
                label().classes("absolute-center text-xs").bind_text_from(
                    self, "value"
                ).tailwind.text_color(text_color)
