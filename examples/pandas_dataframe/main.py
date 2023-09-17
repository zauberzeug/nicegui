#!/usr/bin/env python3
import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype

from nicegui import ui

data={
    'Col_0': [f"Row_{x}" for x in range(1,5)],
    'Col_1': ['This', 'column', 'contains', 'strings.'],
    'Col_2': [x * 4 for x in range(4)],
    'Col_3': [True, False, True, False],
}
df = pd.DataFrame(data)

def update_cell(*, df: pd.DataFrame, r: int, c: int, value):
    df.iat[r, c] = value
    ui.notify(f'(Row_{r+1}, Col_{c}) updated to {value}')

with ui.grid(rows=len(df.index)+1).classes('grid-flow-col'):
    for ic, col in enumerate(df.columns):
        ui.label(col).classes('font-bold')
        for ir, row in enumerate(df.loc[:, col]):
            if ic == 0:
                ui.label(f"{row}")
            else:
                if is_bool_dtype(df[col].dtype):
                    ui_control = ui.checkbox
                elif is_numeric_dtype(df[col].dtype):
                    ui_control = ui.number
                else:
                    ui_control = ui.input

                ui_control(
                    value=row, 
                    on_change=lambda event, r=ir, c=ic: update_cell(df=df, r=r, c=c, value=event.value)
                )

ui.run()
