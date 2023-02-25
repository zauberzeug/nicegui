from typing import Literal, Optional

from ..dependencies import register_component
from ..element import Element
from ..functions.javascript import run_javascript

register_component("qtable", __file__, "qtable.js")


class QTable(Element):
    class Column:
        def __init__(
            self,
            name: str,
            label: str,
            field: str,
            required: Optional[bool] = None,
            align: Optional[str] = None,
            sortable: Optional[bool] = None,
            sort: Optional[str] = None,
            sortOrder: Optional[str] = None,
        ) -> None:
            self.name = name
            self.label = label
            self.field = field

            if required is not None:
                self.required = required

            if align is not None:
                self.align = align

            if sortable is not None:
                self.sortable = sortable

            if sort is not None:
                self.sort = sort

            if sortOrder is not None:
                self.sortOrder = sortOrder

    def __init__(
        self,
        columns: Optional[list[Column]] = [],
        rows: Optional[list] = [],
        title: Optional[str] = None,
        selection_mode: Optional[Literal["single", "multiple", "none"]] = "none",
        selection_key: Optional[str] = "",
    ):
        """QTable
        """

        super().__init__("qtable")

        self._props["columns"] = [col.__dict__ for col in columns]
        self._props["rows"] = rows

        self._props["title"] = title

        self._props["selection_mode"] = selection_mode
        self._props["selection_key"] = selection_key

        self.selected = []
        self.on("selected", handler=self.handle_selected_event)

        self.saved_data = None

    def handle_selected_event(self, data):
        self.selected = data["args"]

    def handle_filter(self, search_field):
        query_string = search_field.value

        # save current data
        if self.saved_data is None:
            self.saved_data = self._props["rows"]

        filtered_data = [
            row
            for row in self.saved_data
            if row.__repr__().lower().find(query_string) is not -1
        ]

        self._props["rows"] = filtered_data
        self.update()
        self.run_method("evalFunction")

    async def __dump__(self):
        await run_javascript(f"console.info(getElement({self.id}))", respond=False)
