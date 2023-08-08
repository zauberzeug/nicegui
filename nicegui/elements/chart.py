from typing import Callable, Dict, List, Optional

from ..element import Element
from ..events import (ChartEventArguments, ChartPointEventArguments, ChartSeriesEventArguments, GenericEventArguments,
                      handle_event)
from ..helpers import KWONLY_SLOTS


class Chart(Element,
            component='chart.js',
            libraries=['lib/highcharts/*.js'],
            extra_libraries=['lib/highcharts/modules/*.js']):

    def __init__(self, options: Dict, *,
                 type: str = 'chart', extras: List[str] = [],
                 on_event: Optional[Callable] = None,
                 on_drag_drop: Optional[Callable] = None) -> None:
        """Chart

        An element to create a chart using `Highcharts <https://www.highcharts.com/>`_.
        Updates can be pushed to the chart by changing the `options` property.
        After data has changed, call the `update` method to refresh the chart.

        By default, a `Highcharts.chart` is created.
        To use, e.g., `Highcharts.stockChart` instead, set the `type` property to "stockChart".

        :param options: dictionary of Highcharts options
        :param type: chart type (e.g. "chart", "stockChart", "mapChart", ...; default: "chart")
        :param extras: list of extra dependencies to include (e.g. "annotations", "arc-diagram", "solid-gauge", ...)
        :param on_change: callback to execute when value changes
        """
        super().__init__()
        self._props['type'] = type
        self._props['options'] = options
        self._props['extras'] = extras
        self.libraries.extend(library for library in self.extra_libraries if library.path.stem in extras)
        if on_event is not None:
            self._props['on_event_set'] = True
        if on_drag_drop is not None:
            self._props['on_drag_drop_set'] = True
        self._on_event = on_event
        self._on_drag_drop = on_drag_drop
        self.on('on_event', self.handle_event)
        self.on('on_point_drag_drop', self.handle_drag_drop)

    def handle_event(self, e: ChartEventArguments) -> None:
        event_type = e.args.get('event_type', None)
        if event_type == 'point_click':
            arguments = ChartPointEventArguments(
                sender=self,
                client=self.client,
                event_type=event_type,
                point_index=e.args.get('point_index', None),
                point_x=e.args.get('point_x', None),
                point_y=e.args.get('point_y', None),
                series_index=e.args.get('series_index', None),
            )
        else:
            arguments = ChartEventArguments(
                sender=self,
                client=self.client,
                event_type=event_type,
            )

        handle_event(self._on_event, arguments)

    def handle_drag_drop(self, e: ChartEventArguments) -> None:
        event_type = e.args.get('event_type', None)
        if event_type == 'point_drag_start':
            arguments = ChartEventArguments(
                sender=self,
                client=self.client,
                event_type=event_type,
            )
        elif event_type == 'point_drag':
            arguments = ChartPointEventArguments(
                sender=self,
                client=self.client,
                event_type=event_type,
                point_index=e.args.get('point_index', None),
                point_x=e.args.get('point_x', None),
                point_y=e.args.get('point_y', None),
                series_index=e.args.get('series_index', None),
            )
        elif event_type == 'point_drop':
            arguments = ChartSeriesEventArguments(
                sender=self,
                client=self.client,
                event_type=event_type,
                point_index=e.args.get('point_index', None),
                point_x=e.args.get('point_x', None),
                point_y=e.args.get('point_y', None),
                series_index=e.args.get('series_index', None),
                series_name=e.args.get('series_name', None),
                series_x=e.args.get('series_x', None),
                series_y=e.args.get('series_y', None),
            )
        handle_event(self._on_drag_drop, arguments)

    @property
    def options(self) -> Dict:
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_chart')
