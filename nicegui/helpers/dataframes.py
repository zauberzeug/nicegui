"""Conversion of Pandas and Polars DataFrames into records for table-like elements."""
import itertools
from typing import TYPE_CHECKING, Any

from .warnings import warn_once

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl


def pandas_to_records(df: 'pd.DataFrame') -> tuple[list[dict], list[Any], list[Any]]:
    """Convert a Pandas DataFrame into records, the corresponding column keys and the original column labels.

    Duplicate column labels are numbered to get unique keys (e.g. "a_0" and "a_1"),
    while the labels keep the original names.
    Columns which cannot be serialized to JSON (datetimes, timedeltas, complex numbers,
    objects, periods and intervals) are converted to strings.
    """
    import pandas as pd  # pylint: disable=import-outside-toplevel

    if isinstance(df.columns, pd.MultiIndex):
        raise ValueError('MultiIndex columns are not supported. '
                         'You can convert them to strings using something like '
                         '`df.columns = ["_".join(col) for col in df.columns.values]`.')

    if not isinstance(df.index, pd.RangeIndex) or df.index.name is not None:
        df = df.reset_index()

    labels = df.columns
    is_duplicate = labels.duplicated(keep=False)
    if is_duplicate.any():
        taken = set(labels)

        def unique_key(label: Any) -> str:
            key = next(f'{label}_{i}' for i in itertools.count() if f'{label}_{i}' not in taken)
            taken.add(key)
            return key

        df = df.set_axis([unique_key(label) if duplicate else label
                          for label, duplicate in zip(labels, is_duplicate, strict=True)], axis=1)
        duplicate_labels = sorted({str(label) for label in labels[is_duplicate]})
        warn_once(f'The Pandas DataFrame has duplicate column names {duplicate_labels}. '
                  'Their row keys are numbered to keep them unique, while the column labels stay unchanged.')

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

    return df.to_dict('records'), list(df.columns), list(labels)


def polars_to_records(df: 'pl.DataFrame') -> tuple[list[dict], list[str]]:
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
    for column in special_cols:
        for row in rows:
            row[column] = to_string(row[column])
    return rows, list(df.columns)
