from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from ...element import Element

if TYPE_CHECKING:
    import numpy as np


class UPlot(Element, component='uplot.js', esm={'nicegui-uplot': 'dist'}, default_classes='nicegui-uplot'):

    def __init__(self, options: dict, data: list | np.ndarray, *, keep_zoom: bool = True) -> None:
        """uPlot

        An element to create a chart using `uPlot <https://leeoniya.github.io/uPlot/>`_.
        The chart fills its element, which can be sized with classes or styles like other elements.

        *Added in version 3.19.0*

        :param options: chart options (see `uPlot options <https://github.com/leeoniya/uPlot/tree/master/docs#basics>`_); ``width`` and ``height`` are ignored
        :param data: chart data (see `uPlot data format <https://github.com/leeoniya/uPlot/tree/master/docs#data-format>`_)
        :param keep_zoom: whether data updates keep the current scales while the x axis is zoomed or panned; otherwise all scales are refit to the new data (default: ``True``)
        """
        super().__init__()
        self.add_resource(Path(__file__).parent / 'dist')
        self._props['options'] = options
        self._props['data'] = data
        self._props['keepZoom'] = keep_zoom

    @property
    def options(self) -> dict:
        """The options dictionary."""
        return self._props['options']

    @options.setter
    def options(self, value: dict) -> None:
        self._props['options'] = value

    @property
    def data(self) -> list | np.ndarray:
        """The data array."""
        return self._props['data']

    @data.setter
    def data(self, value: list | np.ndarray) -> None:
        self._props['data'] = value
