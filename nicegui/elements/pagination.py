from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Pagination(ValueElement, DisableableElement):

    @resolve_defaults
    def __init__(self,
                 min: int, max: int, *,  # pylint: disable=redefined-builtin
                 direction_links: bool = DEFAULT_PROP | False,
                 value: int | None = DEFAULT_PROPS['model-value'] | ...,  # type: ignore
                 on_change: Handler[ValueChangeEventArguments] | None = None) -> None:
        """Pagination

        A pagination element wrapping Quasar's `QPagination <https://quasar.dev/vue-components/pagination>`_ component.

        :param min: minimum page number
        :param max: maximum page number
        :param direction_links: whether to show first/last page links
        :param value: initial page (defaults to `min` if no value is provided)
        :param on_change: callback to be invoked when the value changes
        """
        if value is ...:
            value = min
        super().__init__(tag='q-pagination', value=value, on_value_change=on_change)
        self._props['min'] = min
        self._props['max'] = max
        self._props['direction-links'] = direction_links

    @property
    def min(self) -> int:
        """Minimum page number"""
        return self._props['min']

    @min.setter
    def min(self, value: int) -> None:
        self._props['min'] = value

    @property
    def max(self) -> int:
        """Maximum page number"""
        return self._props['max']

    @max.setter
    def max(self, value: int) -> None:
        self._props['max'] = value

    @property
    def direction_links(self) -> bool:
        """Whether to show first/last page links"""
        return self._props['direction-links']

    @direction_links.setter
    def direction_links(self, value: bool) -> None:
        self._props['direction-links'] = value
