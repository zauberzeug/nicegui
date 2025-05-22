from nicegui import ui

from . import doc


@doc.demo(ui.log)
def main_demo() -> None:
    from datetime import datetime

    log = ui.log(max_lines=10).classes('w-full h-20')
    ui.button('Log time', on_click=lambda: log.push(datetime.now().strftime('%X.%f')[:-5]))


@doc.demo('Attach to a logger', '''
    You can attach a `ui.log` element to a Python logger object so that log messages are pushed to the log element.
    When used inside a page function, it is important to remove the handler when the client disconnects.
    Otherwise, the handler will keep a reference to the log element and the latter will not be garbage collected.
''')
def logger_handler():
    import logging
    from datetime import datetime

    logger = logging.getLogger()

    class LogElementHandler(logging.Handler):
        """A logging handler that emits messages to a log element."""

        def __init__(self, element: ui.log, level: int = logging.NOTSET) -> None:
            self.element = element
            super().__init__(level)

        def emit(self, record: logging.LogRecord) -> None:
            try:
                msg = self.format(record)
                self.element.push(msg)
            except Exception:
                self.handleError(record)

    # @ui.page('/')
    def page():
        log = ui.log(max_lines=10).classes('w-full')
        handler = LogElementHandler(log)
        logger.addHandler(handler)
        ui.context.client.on_disconnect(lambda: logger.removeHandler(handler))
        ui.button('Log time', on_click=lambda: logger.warning(datetime.now().strftime('%X.%f')[:-5]))
    page()  # HIDE


@doc.demo('Styling lines', '''
    On the basis that individual lines in `ui.log` are `ui.label` instances,
    it is possible to style the inserted lines via `classes`, `style` and `props`.
    One notable use would be colored logs.

    Note that if applied, this would clear any existing
    [classes](element#default_classes),
    [style](element#default_style), and
    [props](element#default_props)
    currently set as default on `ui.label`.

    *Added in version 2.18.0*
''')
def styling_lines_demo():
    log = ui.log(max_lines=10).classes('w-full h-40')
    with ui.row():
        ui.button('Normal', on_click=lambda: log.push('Text'))
        ui.button('Debug', on_click=lambda: log.push('Debug', classes='text-grey'))
        ui.button('Info', on_click=lambda: log.push('Info', classes='text-blue'))
        ui.button('Warning', on_click=lambda: log.push('Warning', classes='text-orange'))
        ui.button('Error', on_click=lambda: log.push('Error', classes='text-red'))


doc.reference(ui.log)
