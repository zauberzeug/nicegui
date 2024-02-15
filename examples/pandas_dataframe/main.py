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
    """
    Update the value at the specified row and column in the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to update.
        r (int): The row index.
        c (int): The column index.
        value: The new value to set.

    Returns:
        None

    Raises:
        None

    Example:
        >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        >>> update(df=df, r=1, c=0, value=10)
        >>> print(df)
           A  B
        0  1  4
        1  10 5
        2  3  6
    """
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
