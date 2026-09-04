from .. import helpers, optional_features
from ..element import Element
from .markdown import Markdown

try:
    from nicegui_highcharts import highchart
    optional_features.register('highcharts')
    __all__ = ['highchart']
except ImportError:
    class highchart(Element):  # type: ignore
        def __init__(self, *args, **kwargs) -> None:  # pylint: disable=unused-argument
            """Highcharts chart

            An element to create a chart using `Highcharts <https://www.highcharts.com/>`_.
            Updates can be pushed to the chart by changing the `options` property.

            Due to Highcharts' restrictive license, this element is not part of the standard NiceGUI package.
            It is maintained in a `separate repository <https://github.com/zauberzeug/nicegui-highcharts/>`_
            and can be installed with `pip install nicegui[highcharts]`.
            """
            super().__init__()
            Markdown('Highcharts is not installed. Please run `pip install nicegui[highcharts]`.')
            helpers.warn_once('Highcharts is not installed. Please run "pip install nicegui[highcharts]".')
