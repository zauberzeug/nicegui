from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any, Protocol

import numpy as np

try:
    from tsdownsample import MinMaxLTTBDownsampler  # type: ignore[import-untyped]
    _USE_TSDOWNSAMPLE = True
except ImportError:
    MinMaxLTTBDownsampler = None  # type: ignore[misc,assignment]
    _USE_TSDOWNSAMPLE = False


class Downsampler(Protocol):
    """Protocol for downsampling algorithms."""

    def downsample(self, x: np.ndarray, y: np.ndarray, *, n_out: int) -> np.ndarray:
        """Downsample data to n_out points, returning indices of selected points."""


class _NumpyLTTBDownsampler:
    """Pure NumPy implementation of LTTB (Largest Triangle Three Buckets) algorithm.

    This is a fallback when tsdownsample is not installed. While slower than the
    Rust-based tsdownsample, it produces good visual results for time series data.
    """

    def downsample(self, x: np.ndarray, y: np.ndarray, *, n_out: int) -> np.ndarray:
        """Downsample data using the LTTB algorithm.

        :param x: x-axis values (must be sorted)
        :param y: y-axis values
        :param n_out: target number of output points
        :return: indices of selected points
        """
        n = len(x)
        if n_out >= n:
            return np.arange(n, dtype=np.uint64)
        if n_out < 3:
            # Edge case: return first and last
            return np.array([0, n - 1], dtype=np.uint64) if n_out == 2 else np.array([0], dtype=np.uint64)

        indices = np.empty(n_out, dtype=np.uint64)
        indices[0] = 0  # Always include first point
        indices[n_out - 1] = n - 1  # Always include last point

        # Bucket size for the middle points
        bucket_size = (n - 2) / (n_out - 2)

        prev_idx = 0
        for i in range(1, n_out - 1):
            # Current bucket boundaries
            bucket_start = int((i - 1) * bucket_size) + 1
            bucket_end = int(i * bucket_size) + 1
            bucket_end = min(bucket_end, n - 1)

            # Next bucket boundaries for calculating average point
            next_bucket_start = int(i * bucket_size) + 1
            next_bucket_end = int((i + 1) * bucket_size) + 1
            next_bucket_end = min(next_bucket_end, n)

            # Average point of next bucket
            if next_bucket_start < next_bucket_end:
                avg_x = np.mean(x[next_bucket_start:next_bucket_end])
                avg_y = np.mean(y[next_bucket_start:next_bucket_end])
            else:
                avg_x, avg_y = x[n - 1], y[n - 1]

            # Find point in current bucket that forms largest triangle
            prev_x, prev_y = x[prev_idx], y[prev_idx]

            # Triangle area = 0.5 * |x1(y2-y3) + x2(y3-y1) + x3(y1-y2)|
            # We can skip the 0.5 since we only compare relative areas
            bucket_x = x[bucket_start:bucket_end]
            bucket_y = y[bucket_start:bucket_end]

            areas = np.abs(
                prev_x * (bucket_y - avg_y) +
                bucket_x * (avg_y - prev_y) +
                avg_x * (prev_y - bucket_y)
            )

            max_area_idx = bucket_start + int(np.argmax(areas))
            indices[i] = max_area_idx
            prev_idx = max_area_idx

        return indices


@dataclass
class HFTraceData:
    """High-frequency trace data for resampling.

    ``x`` and ``y`` are the original (dtype-preserving) values, while ``x_num`` and ``y_num`` are
    their float64 views used by the downsampling algorithm and for range masking.
    Keeping both lets the resampled output preserve datetime and integer dtypes instead of
    collapsing everything to floats.
    """
    x: np.ndarray
    y: np.ndarray
    x_num: np.ndarray
    y_num: np.ndarray
    trace_idx: int


def as_array(values: Any) -> np.ndarray:
    """Convert a Plotly trace value to a 1-D NumPy array.

    Plotly encodes NumPy arrays as a binary typed-array dict (``{'dtype': 'f8', 'bdata': '<base64>'}``)
    when a figure is serialized, so a plain ``np.asarray`` would turn that into a useless 0-D object array.
    This decodes that form and otherwise falls back to ``np.asarray`` for plain lists/arrays.
    """
    if isinstance(values, dict) and 'bdata' in values:
        decoded = np.frombuffer(base64.b64decode(values['bdata']), dtype=np.dtype(values['dtype']))
        shape = values.get('shape')
        if shape:
            decoded = decoded.reshape([int(dim) for dim in str(shape).split(',')])
        return decoded
    return np.asarray(values)


def _datetime_to_float(values: np.ndarray) -> np.ndarray:
    """Convert datetime-like data to epoch nanoseconds as float64, mapping ``NaT`` to ``NaN``."""
    as_datetime = values.astype('datetime64[ns]')
    result = as_datetime.astype(np.float64)
    result[np.isnat(as_datetime)] = np.nan  # so missing timestamps are dropped by the NaN filter
    return result


def to_numeric(values: np.ndarray) -> np.ndarray | None:
    """Return a float64 view of ``values`` for use by the downsampling algorithm.

    Numeric data is cast directly; datetime-like data (``datetime64`` arrays or object/string
    arrays of dates, as used for Plotly time axes) is converted to epoch nanoseconds so it can be
    resampled. Returns ``None`` if ``values`` cannot be interpreted numerically, in which case the
    trace should be left untouched rather than raising.
    """
    if np.issubdtype(values.dtype, np.number):
        return values.astype(np.float64)
    if np.issubdtype(values.dtype, np.datetime64):
        return _datetime_to_float(values)
    # For object/string arrays, try plain numbers first so numeric strings ('1', '2') and ``None``
    # behave like floats, and only then fall back to parsing date strings / datetime objects.
    try:
        return values.astype(np.float64)
    except (ValueError, TypeError):
        pass
    try:
        return _datetime_to_float(values)
    except (ValueError, TypeError):
        return None


def create_downsampler() -> Downsampler:
    """Create a downsampler instance, preferring tsdownsample if available."""
    if _USE_TSDOWNSAMPLE:
        return MinMaxLTTBDownsampler()
    return _NumpyLTTBDownsampler()
