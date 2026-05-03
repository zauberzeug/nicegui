from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ...element import Element

if TYPE_CHECKING:
    import numpy as np


class UPlot(Element, component='uplot.js', esm={'nicegui-uplot': 'dist'}):
    def __init__(
        self,
        options: dict,
        data: list[list[Any] | np.ndarray] | np.ndarray,
        scale_mode: str = 'reset',
    ) -> None:
        """
        uPlot Element

        Renders a uPlot chart.

        :param options: uPlot options dictionary (see https://github.com/leeoniya/uPlot/tree/master/docs#basics)
        :param data: uPlot data array (see https://github.com/leeoniya/uPlot/tree/master/docs#data-format)
        :param scale_mode: How to handle plot scale updates when new data arrives. One of 'reset', 'preserve_all', 'preserve_zoom'. (default: 'reset')
        """
        super().__init__()
        self._props['options'] = options
        self._props['data'] = data
        self._props['scaleMode'] = scale_mode


    @property
    def options(self) -> dict:
        """The options dictionary."""
        return self._props['options']

    @property
    def data(self) -> list:
        """The data array."""
        return self._props['data']

    @data.setter
    def data(self, value: list) -> None:
        """Set the data array."""
        self._props['data'] = value
