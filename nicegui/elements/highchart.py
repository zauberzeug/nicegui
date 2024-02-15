from .. import optional_features
from ..element import Element
from ..logging import log
from .markdown import Markdown

try:
    from nicegui_highcharts import highchart
    optional_features.register('highcharts')
    __all__ = ['highchart']
except ImportError:
    class highchart(Element):  # type: ignore
        def __init__(self, *args, **kwargs) -> None:  # pylint: disable=unused-argument
            """Highcharts chart

            An element to create a chart using Highcharts.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Notes:
                - Updates can be pushed to the chart by changing the `options` property.
                - After data has changed, call the `update` method to refresh the chart.

            Raises:
                None

            Examples:
                To create a basic Highcharts chart:

                ```python
                chart = highchart()
                chart.options = {
                    'chart': {
                        'type': 'line'
                    },
                    'title': {
                        'text': 'My Chart'
                    },
                    'series': [{
                        'data': [1, 2, 3, 4, 5]
                    }]
                }
                chart.update()
                ```

            Warnings:
                Due to Highcharts' restrictive license, this element is not part of the standard NiceGUI package.
                It is maintained in a separate repository and can be installed with `pip install nicegui[highcharts]`.

            """
            super().__init__()
            Markdown('Highcharts is not installed. Please run `pip install nicegui[highcharts]`.')
            log.warning('Highcharts is not installed. Please run "pip install nicegui[highcharts]".')
