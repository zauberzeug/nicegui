from __future__ import annotations

from typing import Any

import numpy as np

from ...element import Element


class UPlot(Element, component='uplot.js', esm={'nicegui-uplot': 'dist'}):
    def __init__(
        self,
        options: dict,
        data: list[list[Any] | np.ndarray] | np.ndarray,
        reset_scales: bool = True,
    ) -> None:
        """
        uPlot Element

        Renders a uPlot chart.

        :param options: uPlot options dictionary (see https://github.com/leeoniya/uPlot/tree/master/docs#basics)
        :param data: uPlot data array (see https://github.com/leeoniya/uPlot/tree/master/docs#data-format)
        :param reset_scales: Whether to reset scales when updating data (default: True)
        """
        super().__init__()
        self._props['options'] = options
        self._props['data'] = data
        self._props['resetScales'] = reset_scales

    def update_data(
        self,
        data: list[list[Any] | np.ndarray] | np.ndarray,
    ) -> None:
        """
        Update the data array and optionally reset scales.
        """
        with self._props.suspend_updates():
            self._props['data'] = data
        super().update()

    def update_options(self, options: dict) -> None:
        """
        Update the uPlot options.
        """
        with self._props.suspend_updates():
            self._props['options'] = options
        super().update()
