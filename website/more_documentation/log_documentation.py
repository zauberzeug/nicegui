from nicegui import ui
from website.documentation_tools import text_demo


def main_demo() -> None:
    from datetime import datetime

    log = ui.log(max_lines=10).classes('w-full h-20')
    ui.button('Log time', on_click=lambda: log.push(datetime.now().strftime('%X.%f')[:-5]))


def more() -> None:
    @text_demo('Attach to a logger', '''
        You can attach a `ui.log` element to a Python logger object so that log messages are pushed to the log element.
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
                except (KeyboardInterrupt, SystemExit):
                    raise
                except Exception:
                    self.handleError(record)

        log = ui.log(max_lines=10).classes('w-full')
        logger.addHandler(LogElementHandler(log))
        ui.button('Log time', on_click=lambda: logger.warning(datetime.now().strftime('%X.%f')[:-5]))
