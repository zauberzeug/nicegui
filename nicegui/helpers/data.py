from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


def is_default_range_index(df: pd.DataFrame) -> bool:
    """Check whether the DataFrame uses pandas' default unnamed ``RangeIndex(0, n, 1)``.

    Used by ``from_pandas`` helpers to decide whether to call ``df.reset_index()``
    so that named, custom-range, or MultiIndex data is preserved as columns.
    """
    import pandas as pd  # pylint: disable=import-outside-toplevel
    return (
        isinstance(df.index, pd.RangeIndex)
        and df.index.name is None
        and df.index.start == 0
        and df.index.step == 1
    )
