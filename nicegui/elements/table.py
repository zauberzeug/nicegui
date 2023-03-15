from typing import Callable, Optional

from typing_extensions import Literal

from .mixins.value_element import ValueElement
from ..element import Element


class Tr(Element):
    def __init__(self) -> None:
        super().__init__('q-tr')


class Th(Element):
    def __init__(self) -> None:
        super().__init__('q-th')


class Td(Element):
    def __init__(self, key: str = '') -> None:
        super().__init__('q-td')
        if key:
            self._props['key'] = key


class Table(ValueElement):
    VALUE_PROP = 'filter'

    # Scope table element as Table class attributes.
    row = Tr
    header = Th
    cell = Td

    def __init__(
            self,
            columns: Optional[list] = None,
            rows: Optional[list] = None,
            title: Optional[str] = None,
            selection: Optional[Literal['single', 'multiple', 'none']] = 'none',
            on_filter_change: Optional[Callable] = None,
    ) -> None:
        """Table

        A component that allows you to display using `QTable <https://quasar.dev/vue-components/table>` component.

        :param columns: A list of column objects (see `column API <https://quasar.dev/vue-components/table#qtable-api>`)
        :param rows: A list of row objects.
        :param title: The title of the table.
        :param selection: defines the selection behavior.
            'single': only one cell can be selected at a time.
            'multiple': more than one cell can be selected at a time.
            'none': no cells can be selected.
        """

        super().__init__(tag='q-table', value='', on_value_change=on_filter_change)

        if columns is None:
            columns = []
        if rows is None:
            rows = []

        self._props['columns'] = columns
        self._props['rows'] = rows
        self._props['title'] = title


        self.selected: list = []
        self._props['selected'] = self.selected
        self._props['selection'] = selection
        self.on('selection', handler=self.handle_selected_event)

    def handle_selected_event(self, data):
        self.selected = data['args']
        print(self.selected)
        self.update()
