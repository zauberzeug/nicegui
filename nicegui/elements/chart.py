def chart(*args, **kwargs) -> None:
    """
    Deprecated. Please use `ui.highchart` instead.

    This function is deprecated and should not be used anymore. It raises a `RuntimeError` with a message
    instructing the user to install `nicegui[highcharts]` and use `ui.highchart` instead.

    Parameters:
    *args: Variable length argument list.
    **kwargs: Arbitrary keyword arguments.

    Raises:
    RuntimeError: Always raises a `RuntimeError` with a deprecation message.

    Example:
    >>> chart()
    Traceback (most recent call last):
        ...
    RuntimeError: `ui.chart` is now `ui.highchart`. Please install `nicegui[highcharts]` and use `ui.highchart` instead.
    """
    # DEPRECATED
    raise RuntimeError('`ui.chart` is now `ui.highchart`. '
                       'Please install `nicegui[highcharts]` and use `ui.highchart` instead.')
