import itertools

import pandas as pd

from .warnings import warn_once


def prepare_pandas_df(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Prepare a pandas dataframe for use in elements

    This function checks if the df is a MultiIndex which is not supported, resets the index, renames duplicate column
    names and converts special datatypes. The return value contains the new dataframe and a list of the old column
    names."""

    if isinstance(df.columns, pd.MultiIndex):
        raise ValueError('MultiIndex columns are not supported. '
                         'You can convert them to strings using something like '
                         '`df.columns = ["_".join(col) for col in df.columns.values]`.')

    if not isinstance(df.index, pd.RangeIndex) or df.index.name is not None:
        df = df.reset_index()

    old_col_names = df.columns
    duplicate_columns = old_col_names.duplicated(False)
    if duplicate_columns.any():
        taken = set(old_col_names)

        def unique_name(label) -> str:
            name = next(f'{label}_{i}' for i in itertools.count() if f'{label}_{i}' not in taken)
            taken.add(name)
            return name

        df = df.set_axis([unique_name(label) if is_duplicate else label
                          for label, is_duplicate in zip(old_col_names, duplicate_columns, strict=True)], axis=1)
        duplicate_labels = sorted({str(label) for label in old_col_names[duplicate_columns]})
        warn_once(f'The pandas DataFrame has duplicate column names ({duplicate_labels}). '
                  f'Dictionary keys will be numbered to keep them unique, while the UI will keep the original names.')

    def is_special_dtype(dtype):
        return (pd.api.types.is_datetime64_any_dtype(dtype) or
                pd.api.types.is_timedelta64_dtype(dtype) or
                pd.api.types.is_complex_dtype(dtype) or
                pd.api.types.is_object_dtype(dtype) or
                isinstance(dtype, (pd.PeriodDtype, pd.IntervalDtype)))
    special_cols = df.columns[df.dtypes.apply(is_special_dtype)]
    if not special_cols.empty:
        df = df.copy(deep=False)
        df[special_cols] = df[special_cols].astype(str)

    return df, old_col_names
