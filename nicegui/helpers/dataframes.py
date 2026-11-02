"""Conversion of Pandas and Polars DataFrames into records for table-like elements."""
from typing import Any


def pandas_to_records(df: Any) -> tuple[list[dict], list[Any]]:
    """Convert a Pandas DataFrame into records and the corresponding column labels.

    Columns which cannot be serialized to JSON (datetimes, timedeltas, complex numbers,
    objects, periods and intervals) are converted to strings.
    """
    import pandas as pd  # pylint: disable=import-outside-toplevel

    if not isinstance(df.index, pd.RangeIndex) or df.index.name is not None:
        df = df.reset_index()

    def is_special_dtype(dtype) -> bool:
        return (pd.api.types.is_datetime64_any_dtype(dtype) or
                pd.api.types.is_timedelta64_dtype(dtype) or
                pd.api.types.is_complex_dtype(dtype) or
                pd.api.types.is_object_dtype(dtype) or
                isinstance(dtype, (pd.PeriodDtype, pd.IntervalDtype)))

    special_cols = df.columns[df.dtypes.apply(is_special_dtype)]
    if not special_cols.empty:
        df = df.copy()
        df[special_cols] = df[special_cols].astype(str)

    if isinstance(df.columns, pd.MultiIndex):
        raise ValueError('MultiIndex columns are not supported. '
                         'You can convert them to strings using something like '
                         '`df.columns = ["_".join(col) for col in df.columns.values]`.')

    return df.to_dict('records'), list(df.columns)


def polars_to_records(df: Any) -> tuple[list[dict], list[Any]]:
    """Convert a Polars DataFrame into records and the corresponding column labels.

    Columns which cannot be serialized to JSON (binary, duration and object types)
    are converted to strings.
    """
    import polars as pl  # pylint: disable=import-outside-toplevel

    def is_special_dtype(dtype) -> bool:
        # these dtypes produce bytes, timedelta or arbitrary Python objects, which cannot be serialized to JSON
        return dtype in (pl.Binary, pl.Duration, pl.Object)

    def to_string(value) -> str | None:
        if value is None:  # null values stay empty instead of becoming "None"
            return None
        # decode binary data like Pandas does, but replace undecodable bytes instead of raising
        return value.decode('utf-8', errors='backslashreplace') if isinstance(value, bytes) else str(value)

    special_cols = [name for name, dtype in df.schema.items() if is_special_dtype(dtype)]
    rows = df.to_dicts()
    for row in rows:
        for column in special_cols:
            row[column] = to_string(row[column])
    return rows, list(df.columns)
