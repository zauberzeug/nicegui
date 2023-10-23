try:
    from nicegui_highcharts import highchart
    __all__ = ['highchart']
except ImportError:
    class highchart:  # type: ignore
        def __init__(self, *args, **kwargs) -> None:
            raise NotImplementedError('Highcharts is not installed. Please run `pip install nicegui[highcharts]`.')
