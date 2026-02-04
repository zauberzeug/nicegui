from collections.abc import Callable
from contextlib import suppress
from typing import Literal

from typing_extensions import Self

from ... import optional_features
from ...awaitable_response import AwaitableResponse
from ...defaults import DEFAULT_PROP, resolve_defaults
from ...element import Element
from ...events import (
    EChartComponentClickEventArguments,
    EChartPointClickEventArguments,
    GenericEventArguments,
    Handler,
    handle_event,
)

with suppress(ImportError):
    from pyecharts.charts.base import default, json
    from pyecharts.charts.chart import Base as Chart
    from pyecharts.commons.utils import JsCode
    JS_CODE_MARKER = JsCode('\n').js_code.split('\n')[0]
    optional_features.register('pyecharts')


class EChart(Element, component='echart.js', esm={'nicegui-echart': 'dist'}, default_classes='nicegui-echart'):

    @resolve_defaults
    def __init__(self,
                 options: dict,
                 on_point_click: Handler[EChartPointClickEventArguments] | None = None, *,
                 on_click: Handler[EChartComponentClickEventArguments] | None = None,
                 enable_3d: bool = DEFAULT_PROP | False,
                 renderer: Literal['canvas', 'svg'] = DEFAULT_PROP | 'canvas',
                 theme: str | dict | None = DEFAULT_PROP | None,
                 ) -> None:
        """Apache EChart

        An element to create a chart using `ECharts <https://echarts.apache.org/>`_.
        Updates can be pushed to the chart by changing the `options` property.

        :param options: dictionary of EChart options
        :param on_point_click: callback that is invoked when a point is clicked
        :param on_click: callback that is invoked when any component is clicked (*added in version 3.5.0*)
        :param enable_3d: enforce importing the echarts-gl library
        :param renderer: renderer to use ("canvas" or "svg", *added in version 2.7.0*)
        :param theme: an EChart theme configuration (dictionary or a URL returning a JSON object, *added in version 2.15.0*)
        """
        super().__init__()
        self._props['options'] = options
        self._props['enable-3d'] = enable_3d or any('3D' in key for key in options)
        self._props['renderer'] = renderer
        self._props['theme'] = theme
        self._update_method = 'update_chart'

        if on_point_click:
            self.on_point_click(on_point_click)
        if on_click:
            self.on_click(on_click)

        self._props.add_rename('enable_3d', 'enable-3d')  # DEPRECATED: remove in NiceGUI 4.0

    def on_point_click(self, callback: Handler[EChartPointClickEventArguments]) -> Self:
        """Add a callback to be invoked when a point is clicked."""
        def handle_point_click(e: GenericEventArguments) -> None:
            if e.args['componentType'] != 'series':
                return
            handle_event(callback, EChartPointClickEventArguments(
                sender=self,
                client=self.client,
                component_type=e.args['componentType'],
                series_type=e.args['seriesType'],
                series_index=e.args['seriesIndex'],
                series_name=e.args['seriesName'],
                name=e.args['name'],
                data_index=e.args['dataIndex'],
                data=e.args['data'],
                data_type=e.args.get('dataType'),
                value=e.args['value'],
            ))
        self.on('componentClick', handle_point_click, [
            'componentType',
            'seriesType',
            'seriesIndex',
            'seriesName',
            'name',
            'dataIndex',
            'data',
            'dataType',
            'value',
        ])
        return self

    def on_click(self, callback: Handler[EChartComponentClickEventArguments]) -> Self:
        """Add a callback to be invoked when any component is clicked."""
        def handle_click(e: GenericEventArguments) -> None:
            handle_event(callback, EChartComponentClickEventArguments(
                sender=self,
                client=self.client,
                component_type=e.args['componentType'],
                name=e.args.get('name'),
            ))
        self.on('componentClick', handle_click, [
            'componentType',
            'name',
        ])
        return self

    @classmethod
    def from_pyecharts(cls, chart: 'Chart', on_point_click: Callable | None = None) -> Self:
        """Create an echart element from a pyecharts object.

        :param chart: pyecharts chart object
        :param on_click_point: callback which is invoked when a point is clicked

        :return: echart element
        """
        options = json.loads(json.dumps(chart.get_options(), default=default, ignore_nan=True))
        stack = [options]
        while stack:
            current = stack.pop()
            if isinstance(current, list):
                stack.extend(current)
            elif isinstance(current, dict):
                for key, value in tuple(current.items()):
                    if isinstance(value, str) and value.startswith(JS_CODE_MARKER) and value.endswith(JS_CODE_MARKER):
                        current[f':{key}'] = current.pop(key)[len(JS_CODE_MARKER):-len(JS_CODE_MARKER)]
                    else:
                        stack.append(value)
        return cls(options, on_point_click)

    @property
    def options(self) -> dict:
        """The options dictionary."""
        return self._props['options']

    def run_chart_method(self, name: str, *args, timeout: float = 1) -> AwaitableResponse:
        """Run a method of the EChart instance.

        See the `ECharts documentation <https://echarts.apache.org/en/api.html#echartsInstance>`_ for a list of methods.

        If the function is awaited, the result of the method call is returned.
        Otherwise, the method is executed without waiting for a response.

        :param name: name of the method (a prefix ":" indicates that the arguments are JavaScript expressions)
        :param args: arguments to pass to the method (Python objects or JavaScript expressions)
        :param timeout: timeout in seconds (default: 1 second)

        :return: AwaitableResponse that can be awaited to get the result of the method call
        """
        return self.run_method('run_chart_method', name, *args, timeout=timeout)
