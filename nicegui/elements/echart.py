from typing import Callable, Dict, Optional

from typing_extensions import Self

from .. import optional_features
from ..awaitable_response import AwaitableResponse
from ..element import Element
from ..events import EChartPointClickEventArguments, GenericEventArguments, handle_event

try:
    from pyecharts.charts.base import default, json
    from pyecharts.charts.chart import Base as Chart
    from pyecharts.commons.utils import JsCode
    JS_CODE_MARKER = JsCode('\n').js_code.split('\n')[0]
    optional_features.register('pyecharts')
except ImportError:
    pass


class EChart(Element, component='echart.js', libraries=['lib/echarts/echarts.min.js']):
    """
    A class representing an Apache EChart element.

    This element allows you to create a chart using ECharts (https://echarts.apache.org/).
    Updates can be pushed to the chart by changing the `options` property.
    After data has changed, call the `update` method to refresh the chart.

    Attributes:
        options (dict): The options dictionary for the EChart.
    
    Args:
        options (dict): Dictionary of EChart options.
        on_point_click (Optional[Callable]): Callback function that is called when a point is clicked.

    Methods:
        from_pyecharts(cls, chart: 'Chart', on_point_click: Optional[Callable] = None) -> Self:
            Create an EChart element from a pyecharts object.
        
        update(self) -> None:
            Update the EChart element.
        
        run_chart_method(self, name: str, *args, timeout: float = 1, check_interval: float = 0.01) -> AwaitableResponse:
            Run a method of the EChart instance.

    Example:
        # Create an EChart element
        options = {
            'title': {
                'text': 'EChart Example'
            },
            'xAxis': {
                'type': 'category',
                'data': ['A', 'B', 'C', 'D', 'E']
            },
            'yAxis': {
                'type': 'value'
            },
            'series': [{
                'data': [1, 3, 2, 4, 5],
                'type': 'bar'
            }]
        }
        echart = EChart(options)

        # Update the chart data
        echart.options['series'][0]['data'] = [5, 4, 3, 2, 1]
        echart.update()

        # Run a method of the EChart instance
        echart.run_chart_method('resize')
    """
    def __init__(self, options: Dict, on_point_click: Optional[Callable] = None) -> None:
            """EChart

            Args:
            
                - options (dict): Dictionary of EChart options. This should include all the necessary configurations for the EChart.
                - on_point_click (Optional[Callable]): Optional callback function that is called when a point is clicked.
                    The function should accept a single argument, which is an instance of EChartPointClickEventArguments.

            Returns:
                None
            """
            super().__init__()
            self._props['options'] = options
            self._classes.append('nicegui-echart')

            if on_point_click:
                def handle_point_click(e: GenericEventArguments) -> None:
                    handle_event(on_point_click, EChartPointClickEventArguments(
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

    @classmethod
    def from_pyecharts(cls, chart: 'Chart', on_point_click: Optional[Callable] = None) -> Self:
        """
        Create an EChart element from a pyecharts object.

        Args:
            chart ('Chart'): pyecharts chart object.
            on_point_click (Optional[Callable]): Callback function that is called when a point is clicked.

        Returns:
            EChart: The created EChart element.
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
        """
        Get the options dictionary.

        This method returns the options dictionary associated with the EChart element.
        The options dictionary contains the configuration options for the EChart, such as
        the chart type, data series, axes, and other visual settings.

        Returns:
            dict: The options dictionary.

        Example:
            >>> chart = EChart()
            >>> options = chart.options()
            >>> print(options)
            {'title': {'text': 'My Chart'}, 'xAxis': {'type': 'category', 'data': ['A', 'B', 'C']}, ...}
        """
        return self._props['options']

    def update(self) -> None:
            """
            Update the EChart element.

            This method updates the EChart element by calling the base class's update method
            and then running the 'update_chart' method. It should be called whenever the data
            or configuration of the EChart needs to be updated.

            Returns:
                None
            """
            super().update()
            self.run_method('update_chart')

    def run_chart_method(self, name: str, *args, timeout: float = 1, check_interval: float = 0.01) -> AwaitableResponse:
        """
        Run a method of the EChart instance.

        This method allows you to execute a method of the EChart instance in a separate thread and asynchronously
        wait for the result. It is particularly useful when interacting with JavaScript code from Python.

        Args:
            name (str): The name of the method to be executed. If the name starts with a ":", it indicates that the
                arguments are JavaScript expressions.
            *args: The arguments to pass to the method. These can be Python objects or JavaScript expressions.
            timeout (float, optional): The maximum time to wait for a response, in seconds. If the timeout is exceeded,
                a TimeoutError will be raised. Defaults to 1 second.
            check_interval (float, optional): The interval, in seconds, at which to check for a response. Defaults to
                0.01 seconds.

        Returns:
            AwaitableResponse: An AwaitableResponse object that can be awaited to get the result of the method call.

        Raises:
            TimeoutError: If the method execution exceeds the specified timeout.
        """
        return self.run_method('run_chart_method', name, *args, timeout=timeout, check_interval=check_interval)
