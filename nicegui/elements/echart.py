from typing import Callable, Dict, Literal, Optional

from typing_extensions import Self

from .. import optional_features
from ..awaitable_response import AwaitableResponse
from ..element import Element
from ..events import EChartPointClickEventArguments, GenericEventArguments, Handler, handle_event

try:
    from pyecharts.charts.base import default, json
    from pyecharts.charts.chart import Base as Chart
    from pyecharts.commons.utils import JsCode
    JS_CODE_MARKER = JsCode('\n').js_code.split('\n')[0]
    optional_features.register('pyecharts')
except ImportError:
    pass


class EChart(Element,
             component='echart.js',
             dependencies=['lib/echarts/echarts.min.js', 'lib/echarts-gl/echarts-gl.min.js'],
             default_classes='nicegui-echart'):

    def __init__(self,
                 options: Dict,
                 on_point_click: Optional[Handler[EChartPointClickEventArguments]] = None, *,
                 enable_3d: bool = False,
                 renderer: Literal['canvas', 'svg'] = 'canvas',
                 ) -> None:
        """Apache EChart

        An element to create a chart using `ECharts <https://echarts.apache.org/>`_.
        Updates can be pushed to the chart by changing the `options` property.
        After data has changed, call the `update` method to refresh the chart.

        :param options: dictionary of EChart options
        :param on_click_point: callback that is invoked when a point is clicked
        :param enable_3d: enforce importing the echarts-gl library
        :param renderer: renderer to use ("canvas" or "svg")
        """
        super().__init__()
        self._props['options'] = options
        self._props['enable_3d'] = enable_3d or any('3D' in key for key in options)
        self._props['renderer'] = renderer

        if on_point_click:
            self.on_point_click(on_point_click)

    def on_point_click(self, callback: Handler[EChartPointClickEventArguments]) -> Self:
        """Add a callback to be invoked when a point is clicked."""
        def handle_point_click(e: GenericEventArguments) -> None:
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
        self.on('pointClick', handle_point_click, [
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

    @classmethod
    def from_pyecharts(cls, chart: 'Chart', on_point_click: Optional[Callable] = None) -> Self:
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
    def options(self) -> Dict:
        """The options dictionary."""
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_chart')

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
