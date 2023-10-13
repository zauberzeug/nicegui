from typing import Callable, Dict, List, Optional

from ..element import Element
from ..events import (ChartPointClickEventArguments, ChartPointDragEventArguments, ChartPointDragStartEventArguments,
                      ChartPointDropEventArguments, GenericEventArguments, handle_event)


class Chart(Element,
            component='chart.js',
            libraries=['lib/highcharts/*.js'],
            extra_libraries=['lib/highcharts/modules/*.js']):

    def __init__(self, options: Dict, *,
                 type: str = 'chart', extras: List[str] = [],  # pylint: disable=redefined-builtin
                 on_point_click: Optional[Callable] = None,
                 on_point_drag_start: Optional[Callable] = None,
                 on_point_drag: Optional[Callable] = None,
                 on_point_drop: Optional[Callable] = None,
                 ) -> None:
        """Chart

        An element to create a chart using `Highcharts <https://www.highcharts.com/>`_.
        Updates can be pushed to the chart by changing the `options` property.
        After data has changed, call the `update` method to refresh the chart.

        By default, a `Highcharts.chart` is created.
        To use, e.g., `Highcharts.stockChart` instead, set the `type` property to "stockChart".

        :param options: dictionary of Highcharts options
        :param type: chart type (e.g. "chart", "stockChart", "mapChart", ...; default: "chart")
        :param extras: list of extra dependencies to include (e.g. "annotations", "arc-diagram", "solid-gauge", ...)
        :param on_point_click: callback function that is called when a point is clicked
        :param on_point_drag_start: callback function that is called when a point drag starts
        :param on_point_drag: callback function that is called when a point is dragged
        :param on_point_drop: callback function that is called when a point is dropped
        """
        super().__init__()
        self._props['type'] = type
        self._props['options'] = options
        self._props['extras'] = extras
        self.libraries.extend(library for library in self.extra_libraries if library.path.stem in extras)

        if on_point_click:
            def handle_point_click(e: GenericEventArguments) -> None:
                handle_event(on_point_click, ChartPointClickEventArguments(
                    sender=self,
                    client=self.client,
                    event_type='point_click',
                    point_index=e.args['point_index'],
                    point_x=e.args['point_x'],
                    point_y=e.args['point_y'],
                    series_index=e.args['series_index'],
                ))
            self.on('pointClick', handle_point_click, ['point_index', 'point_x', 'point_y', 'series_index'])

        if on_point_drag_start:
            def handle_point_dragStart(_: GenericEventArguments) -> None:
                handle_event(on_point_drag_start, ChartPointDragStartEventArguments(
                    sender=self,
                    client=self.client,
                    event_type='point_drag_start',
                ))
            self.on('pointDragStart', handle_point_dragStart, [])

        if on_point_drag:
            def handle_point_drag(e: GenericEventArguments) -> None:
                handle_event(on_point_drag, ChartPointDragEventArguments(
                    sender=self,
                    client=self.client,
                    event_type='point_drag',
                    point_index=e.args['point_index'],
                    point_x=e.args['point_x'],
                    point_y=e.args['point_y'],
                    series_index=e.args['series_index'],
                ))
            self.on('pointDrag', handle_point_drag, ['point_index', 'point_x', 'point_y', 'series_index'])

        if on_point_drop:
            def handle_point_drop(e: GenericEventArguments) -> None:
                handle_event(on_point_drop, ChartPointDropEventArguments(
                    sender=self,
                    client=self.client,
                    event_type='point_drop',
                    point_index=e.args['point_index'],
                    point_x=e.args['point_x'],
                    point_y=e.args['point_y'],
                    series_index=e.args['series_index'],
                ))
            self.on('pointDrop', handle_point_drop, ['point_index', 'point_x', 'point_y', 'series_index'])

    @property
    def options(self) -> Dict:
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_chart')
