from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np

try:
    from tsdownsample import MinMaxLTTBDownsampler  # type: ignore[import-untyped]
    _USE_TSDOWNSAMPLE = True
except ImportError:
    MinMaxLTTBDownsampler = None  # type: ignore[misc,assignment]
    _USE_TSDOWNSAMPLE = False


class Downsampler(Protocol):
    """Protocol for downsampling algorithms."""

    def downsample(self, x: np.ndarray, y: np.ndarray, n_out: int) -> np.ndarray:
        """Downsample data to n_out points, returning indices of selected points."""
        ...


class _NumpyLTTBDownsampler:
    """Pure NumPy implementation of LTTB (Largest Triangle Three Buckets) algorithm.

    This is a fallback when tsdownsample is not installed. While slower than the
    Rust-based tsdownsample, it produces good visual results for time series data.
    """

    def downsample(self, x: np.ndarray, y: np.ndarray, n_out: int) -> np.ndarray:
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

            max_area_idx = bucket_start + np.argmax(areas)
            indices[i] = max_area_idx
            prev_idx = max_area_idx

        return indices


@dataclass
class HFTraceData:
    """High-frequency trace data for resampling."""
    x: np.ndarray
    y: np.ndarray
    trace_idx: int


def create_downsampler() -> Downsampler:
    """Create a downsampler instance, preferring tsdownsample if available."""
    if _USE_TSDOWNSAMPLE:
        return MinMaxLTTBDownsampler()
    return _NumpyLTTBDownsampler()
