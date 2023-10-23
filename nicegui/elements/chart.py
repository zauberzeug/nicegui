def chart(*args, **kwargs) -> None:
    """Deprecated. Please use `ui.highchart` instead."""
    # DEPRECATED
    raise RuntimeError('`ui.chart` is now `ui.highchart`. '
                       'Please install `nicegui[highcharts]` and use `ui.highchart` instead.')
