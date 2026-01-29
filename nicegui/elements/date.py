from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Date(ValueElement, DisableableElement):

    @resolve_defaults
    def __init__(self,
                 value: (
                     str | dict[str, str] | list[str] | list[str | dict[str, str]] | None
                 ) = DEFAULT_PROPS['model-value'] | None,
                 *,
                 mask: str = DEFAULT_PROP | 'YYYY-MM-DD',
                 on_change: Handler[ValueChangeEventArguments] | None = None) -> None:
        """Date Picker

        This element is based on Quasar's `QDate <https://quasar.dev/vue-components/date>`_ component.
        The date is a string in the format defined by the `mask` parameter.

        You can also use the `range` or `multiple` props to select a range of dates or multiple dates::

            ui.date({'from': '2023-01-01', 'to': '2023-01-05'}).props('range')
            ui.date(['2023-01-01', '2023-01-02', '2023-01-03']).props('multiple')
            ui.date([{'from': '2023-01-01', 'to': '2023-01-05'}, '2023-01-07']).props('multiple range')

        :param value: the initial date
        :param mask: the format of the date string (default: 'YYYY-MM-DD')
        :param on_change: callback to execute when changing the date
        """
        super().__init__(tag='q-date', value=value, on_value_change=on_change)
        self._props['mask'] = mask
