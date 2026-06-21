from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Literal

from ...element import Element

if TYPE_CHECKING:
    import numpy as np


class UPlot(Element, component='uplot.js', esm={'nicegui-uplot': 'dist'}, default_classes='nicegui-uplot'):

    def __init__(
        self,
        options: dict,
        data: Sequence[Any] | np.ndarray,
        scale_mode: Literal['reset', 'preserve_all', 'preserve_zoom'] = 'reset',
    ) -> None:
        """uPlot

        An element to create a chart using `uPlot <https://leeoniya.github.io/uPlot/>`_.

        :param options: chart options (see `uPlot options <https://github.com/leeoniya/uPlot/tree/master/docs#basics>`_)
        :param data: chart data (see `uPlot data format <https://github.com/leeoniya/uPlot/tree/master/docs#data-format>`_)
        :param scale_mode: how scales are updated on data changes: "reset" (always recompute, default), "preserve_all" (never recompute), or "preserve_zoom" (recompute unless the user is zoomed)
        """
        super().__init__()
        self._props['options'] = options
        self._props['data'] = data
        self._props['scaleMode'] = scale_mode

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
    def data(self) -> list:
        """The data array."""
        return self._props['data']

    @data.setter
    def data(self, value: Sequence[Any] | np.ndarray) -> None:
        self._props['data'] = value
