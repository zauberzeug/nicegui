#!/usr/bin/env python3
import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype

from nicegui import ui

df = pd.DataFrame(data={
    'col1': [x for x in range(4)],
    'col2': ['This', 'column', 'contains', 'strings.'],
    'col3': [x / 4 for x in range(4)],
    'col4': [True, False, True, False],
})


def update(*, df: pd.DataFrame, r: int, c: int, value):
    df.iat[r, c] = value
    ui.notify(f'Set ({r}, {c}) to {value}')


with ui.grid(rows=len(df.index)+1).classes('grid-flow-col'):
    for c, col in enumerate(df.columns):
        ui.label(col).classes('font-bold')
        for r, row in enumerate(df.loc[:, col]):
            if is_bool_dtype(df[col].dtype):
                cls = ui.checkbox
            elif is_numeric_dtype(df[col].dtype):
                cls = ui.number
            else:
                cls = ui.input
            cls(value=row, on_change=lambda event, r=r, c=c: update(df=df, r=r, c=c, value=event.value))

ui.run()
