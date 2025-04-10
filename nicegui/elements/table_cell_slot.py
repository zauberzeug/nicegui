from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Dict

from ..context import context
from ..element import Element
from ..elements.mixins.value_element import ValueElement
from .table_slot_placeholder import TableSlotPlaceholder
from .teleport import Teleport

if TYPE_CHECKING:
    from .table import Table

class TableCellSlot(Element, component="table_cell_slot.js"):
    def __init__(self, table: Table, slot_name: str ,func: Callable[[int,str], None]):
        super().__init__()
        def slot_build_fn(cell_props: Dict):
            class_name = f"--table-slot-{slot_name}-{cell_props['rowIndex']}"
            with Teleport(f"#c{table.id} .{class_name}") as tp:
                func(cell_props['rowIndex'],slot_name)

            # I'm not sure why. But setting LOOPBACK to True makes the slot work.
            for element in tp:
                if isinstance(element, ValueElement):
                    element.LOOPBACK=True
            return tp

        self._slot_build_fn=slot_build_fn
        self.func = func
        self._teleport_slots_cache: Dict[int, Teleport] = {}
        # note: If the component is not instantiated, it cannot be used in table slots.
        TableSlotPlaceholder()
        template = rf"""
        <q-td key="name" :props="props" >
            <nicegui-table_slot_placeholder :tableCellSlotId="{self.id}" :dataProps="props" :class="`--table-slot-{slot_name}-${{props.rowIndex}}`"></nicegui-table_slot_placeholder>
        </q-td>
            """

        def placeholder_updated(e):
            row_props = e.args
            self._create_cell_slot(row_props)

        self.on("placeholder_updated", placeholder_updated)
        table.add_slot(f"body-cell-{slot_name}", template)

        # make sure container is initialized before emitting the init event
        client = context.client
        if client.has_socket_connection:
            self.run_method("setLoaded")
        else:
            def on_connect():
                self.run_method("setLoaded")

            client.on_connect(on_connect)

    def _create_cell_slot(self, row_props:Dict):
        key = row_props['rowIndex']
        tp = self._teleport_slots_cache.get(key, None)
        if tp:
            tp.update()
            return

        with self:
            tp = self._slot_build_fn(row_props)
        self._teleport_slots_cache[key] = tp

    def _handle_delete(self) -> None:
        self._teleport_slots_cache.clear()
        return super()._handle_delete()
