from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ...element import Element

if TYPE_CHECKING:
    import numpy as np


class UPlot(Element, component='uplot.js', esm={'nicegui-uplot': 'dist'}, default_classes='nicegui-uplot'):

    def __init__(
        self,
        options: dict,
        data: Sequence[Any] | np.ndarray,
        *,
        keep_zoom: bool = True,
    ) -> None:
        """uPlot

        An element to create a chart using `uPlot <https://leeoniya.github.io/uPlot/>`_.

        :param options: chart options (see `uPlot options <https://github.com/leeoniya/uPlot/tree/master/docs#basics>`_); ``width`` and ``height`` only set the initial size, the chart follows its element afterwards
        :param data: chart data (see `uPlot data format <https://github.com/leeoniya/uPlot/tree/master/docs#data-format>`_)
        :param keep_zoom: whether data updates keep the current scales while the x axis is zoomed or panned; otherwise all scales are refit to the new data (default: ``True``)

        *Added in version 3.19.0*
        """
        super().__init__()
        self.add_resource(Path(__file__).parent / 'dist')
        self._props['options'] = options
        self._props['data'] = data
        self._props['keepZoom'] = keep_zoom

        if 'width' in options:
            self.style(f'--nicegui-uplot-width: {options["width"]}px')
        if 'height' in options:
            self.style(f'--nicegui-uplot-height: {options["height"]}px')

    @property
    def options(self) -> dict:
        """The options dictionary."""
        return self._props['options']

    @options.setter
    def options(self, value: dict) -> None:
        self._props['options'] = value

    @property
    def data(self) -> Sequence[Any] | np.ndarray:
        """The data array."""
        return self._props['data']

    @data.setter
    def data(self, value: Sequence[Any] | np.ndarray) -> None:
        self._props['data'] = value
