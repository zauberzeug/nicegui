from ..defaults import DEFAULT_PROP, resolve_defaults
from .label import Label as label
from .mixins.color_elements import TextColorElement
from .mixins.value_element import ValueElement


class LinearProgress(ValueElement, TextColorElement):
    VALUE_PROP = 'value'

    @resolve_defaults
    def __init__(self,
                 value: float = DEFAULT_PROP | 0.0, *,
                 size: str | None = DEFAULT_PROP | None,
                 show_value: bool = True,
                 color: str | None = DEFAULT_PROP | 'primary',
                 ) -> None:
        """Linear Progress

        A linear progress bar wrapping Quasar's
        `QLinearProgress <https://quasar.dev/vue-components/linear-progress>`_ component.

        :param value: the initial value of the field (from 0.0 to 1.0)
        :param size: the height of the progress bar (default: "20px" with value label and "4px" without)
        :param show_value: whether to show a value label in the center (default: `True`)
        :param color: color (either a Quasar, Tailwind, or CSS color or `None`, default: "primary")
        """
        super().__init__(tag='q-linear-progress', value=value, on_value_change=None, text_color=color)
        self._props['size'] = size if size is not None else '20px' if show_value else '4px'

        if show_value:
            with self:
                label().classes('absolute-center text-sm text-white').bind_text_from(self, 'value')


class CircularProgress(ValueElement, TextColorElement):
    VALUE_PROP = 'value'

    @resolve_defaults
    def __init__(self,
                 value: float = DEFAULT_PROP | 0.0, *,
                 min: float = DEFAULT_PROP | 0.0,  # pylint: disable=redefined-builtin
                 max: float = DEFAULT_PROP | 1.0,  # pylint: disable=redefined-builtin
                 size: str = DEFAULT_PROP | 'xl',
                 show_value: bool = True,
                 color: str | None = DEFAULT_PROP | 'primary',
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
        super().__init__(tag='q-circular-progress', value=value, on_value_change=None, text_color=color)
        self._props['min'] = min
        self._props['max'] = max
        self._props['size'] = size
        self._props['show-value'] = True  # NOTE always activate the default slot because this is expected by ui.element
        self._props['track-color'] = 'grey-4'

        if show_value:
            with self:
                label().classes('absolute-center text-xs').bind_text_from(self, 'value')
