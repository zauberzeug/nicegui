from nicegui.element import Element


class TableSlotPlaceholder(Element, component="table_slot_placeholder.js"):
    def __init__(self) -> None:
        super().__init__()
        self._props["tableCellSlotId"] = None
        self._props["dataProps"] = None
        self.style("display:none")


