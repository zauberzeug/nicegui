import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype

from nicegui import ui

df = pd.DataFrame(
    data={
        "col1": [x for x in range(6)],
        "col2": ["this", "column", "contains", "strings", "of", "text"],
        "col3": [x / 6 for x in range(6)],
        "col4": [True, False] * 3,
    }
)


def update(*, df: pd.DataFrame, r: int, c: int, value):
    df.iat[r, c] = value
    ui.notify(f"Set ({r}, {c}) to {value}")


def home():
    with ui.row():
        for c, col in enumerate(df.columns):
            with ui.column():
                ui.label(col.capitalize())
                for r, row in enumerate(df.loc[:, col]):
                    with ui.row().classes("h-8 items-center"):
                        if is_numeric_dtype(df[col].dtype):
                            cls = ui.number
                        elif is_bool_dtype(df[col].dtype):
                            cls = ui.checkbox
                        else:
                            cls = ui.input
                        cls(value=row, on_change=lambda event, r=r, c=c: update(df=df, r=r, c=c, value=event.value))


home()
ui.run(native=True)
