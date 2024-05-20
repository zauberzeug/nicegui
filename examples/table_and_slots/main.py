#!/usr/bin/env python3
import time
import typing as ty
from nicegui.elements.aggrid import AgGrid
import random 
from pathlib import Path

from nicegui import ui, app



def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)



rows = [
    {'id': 0, 'name': 'Alice', 'age': 18},
    {'id': 1, 'name': 'Bob', 'age': 21},
    {'id': 2, 'name': 'Lionel', 'age': 19},
    {'id': 3, 'name': 'Michael', 'age': 32},
    {'id': 4, 'name': 'Julie', 'age': 12},
    {'id': 5, 'name': 'Livia', 'age': 25},
    {'id': 6, 'name': 'Carol'},
]

def get_default_column_defs(
    columns: ty.Iterable[str], date_columns: ty.Iterable[str]
):
    column_defs = []
    for i, col in enumerate(columns):
        col_def = dict(
            headerName=col.upper().replace("_", " "),
            checkboxSelection=True if i == 0 else False,
            field=col,
            filter="agDateColumnFilter" if col in date_columns else "agTextColumnFilter",
        )
        if col in date_columns:
            col_def["valueFormatter"] = ui.js("(value) => { value ? new Date(Date.parse(value)) : null }")
            col_def["filterParams"] = ui.js(
                obj="comparator", 
                file=Path(__file__).parent / "test.js", 
                prop="comparator"
            )
        column_defs.append(col_def)
    return column_defs


grid = ui.aggrid(
    options={
        "columnDefs": get_default_column_defs(["name", "birthday"], ["birthday"]),
        "rowData": [
            dict(name=name, birthday=random_date("1/1/2008 1:30 PM", "1/1/2024 4:50 AM", random.random())) 
            for name in ["Joe", "Ashlynn", "Dave", "Bill", "Steve"]
        ],
        "defaultColDef": dict(sortable=True, resizable=True),
        "pagination": "true",
        "rowSelection": "single",
        "onGridReady": ui.js("(params) => params.columnApi.autoSizeAllColumns()"),
    },
)

ui.run()
