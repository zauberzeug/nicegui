import random
import string

import pandas as pd
from pandas.api.types import is_any_real_numeric_dtype, is_bool_dtype

from nicegui import ui


def generate_random_dataframe(*, range_columns=(5, 8), range_rows=(5, 10)):
    """Returns a pandas dataframe with a random number of rows and columns, each
    containing random data of various data types.
    """

    # Generate random number of columns
    num_columns = random.randint(*range_columns)

    # Generate random column names
    column_names = [''.join(random.choices(string.ascii_letters, k=random.randint(3, 10))) for i in range(num_columns)]

    # Generate random data types for each column
    column_types = [random.choice([int, float, str, bool]) for i in range(num_columns)]

    # Generate random data for each row
    rows = []
    num_rows = random.randint(*range_rows)
    for i in range(num_rows):
        row = []
        for j in range(num_columns):
            if column_types[j] == int:
                row.append(random.randint(-100, 100))
            elif column_types[j] == float:
                row.append(random.uniform(-100, 100))
            elif column_types[j] == str:
                row.append(''.join(random.choices(string.ascii_letters, k=random.randint(3, 10))))
            elif column_types[j] == bool:
                row.append(random.choice([True, False]))
        rows.append(row)

    # Add a column with integers and the same name as another column
    column_name = random.choice(column_names)
    column_names.append(column_name + ' ID')
    column_types.append(int)
    for row in rows:
        row.append(random.randint(1, 100))

    # Create the dataframe
    return pd.DataFrame(rows, columns=column_names)


# Basic formatting
row_height = "h-8"


def update(*, df, coordinates, change):
    """Updates the dataframe as changes are made to the UI's controls.
    """
    x, y = coordinates[change.sender]
    df.iat[y, x] = change.value
    ui.notify(f"Set ({x}, {y}) to {change.value}")


@ui.refreshable
def home():
    """Show the editable pandas dataframe in a nicgui UI. A new dataframe is generated
    each time this function is refreshed (i.e.: each time it is called).
    """

    # Use a random dataframe each refresh
    df = generate_random_dataframe()

    # To match controls with dataframe cells
    coordinates = dict()

    with ui.header():
        ui.button("Randomize", on_click=home.refresh)

    with ui.row():
        for i, col in enumerate(df.columns):
            with ui.column():
                with ui.row():
                    ui.label(col.capitalize())
                for j, row in enumerate(df.loc[:, col]):
                    with ui.row().classes(f"{row_height} items-center"):
                        if is_any_real_numeric_dtype(df[col].dtype):
                            coordinates[ui.number(
                                value=row,
                                on_change=lambda x: update(
                                    df=df,
                                    coordinates=coordinates,
                                    change=x,
                                ))] = (i, j)
                        elif is_bool_dtype(df[col].dtype):
                            coordinates[ui.checkbox(
                                value=row,
                                on_change=lambda x: update(
                                    df=df,
                                    coordinates=coordinates,
                                    change=x,
                                ))] = (i, j)
                        else:
                            coordinates[ui.input(
                                value=row,
                                on_change=lambda x: update(
                                    df=df,
                                    coordinates=coordinates,
                                    change=x,
                                ))] = (i, j)


home()
ui.run(native=True)