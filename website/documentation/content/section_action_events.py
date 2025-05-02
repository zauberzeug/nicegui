from nicegui import app, ui

from . import (
    clipboard_documentation,
    doc,
    generic_events_documentation,
    keyboard_documentation,
    refreshable_documentation,
    run_javascript_documentation,
    storage_documentation,
    timer_documentation,
)

doc.title('Action & *Events*')

doc.intro(timer_documentation)
doc.intro(keyboard_documentation)


@doc.demo('UI Updates', '''
    NiceGUI tries to automatically synchronize the state of UI elements with the client,
    e.g. when a label text, an input value or style/classes/props of an element have changed.
    In other cases, you can explicitly call `element.update()` or `ui.update(*elements)` to update.
    The demo code shows both methods for a `ui.echart`, where it is difficult to automatically detect changes in the `options` dictionary.
''')
def ui_updates_demo():
    from random import random

    chart = ui.echart({
        'xAxis': {'type': 'value'},
        'yAxis': {'type': 'value'},
        'series': [{'type': 'line', 'data': [[0, 0], [1, 1]]}],
    })

    def add():
        chart.options['series'][0]['data'].append([random(), random()])
        chart.update()

    def clear():
        chart.options['series'][0]['data'].clear()
        ui.update(chart)

    with ui.row():
        ui.button('Add', on_click=add)
        ui.button('Clear', on_click=clear)


doc.intro(refreshable_documentation)


@doc.demo('Async event handlers', '''
    Most elements also support asynchronous event handlers.

    Note: You can also pass a `functools.partial` into the `on_click` property to wrap async functions with parameters.
''')
def async_handlers_demo():
    import asyncio

    async def async_task():
        ui.notify('Asynchronous task started')
        await asyncio.sleep(5)
        ui.notify('Asynchronous task finished')

    ui.button('start async task', on_click=async_task)


doc.intro(generic_events_documentation)


@doc.demo('Running CPU-bound tasks', '''
    NiceGUI provides a `cpu_bound` function for running CPU-bound tasks in a separate process.
    This is useful for long-running computations that would otherwise block the event loop and make the UI unresponsive.
    The function returns a future that can be awaited.

    Note:
    The function needs to transfer the whole state of the passed function to the process, which is done with pickle.
    It is encouraged to create free functions or static methods which get all the data as simple parameters (i.e. no class or UI logic)
    and return the result, instead of writing it in class properties or global variables.
''')
def cpu_bound_demo():
    import time

    from nicegui import run

    def compute_sum(a: float, b: float) -> float:
        time.sleep(1)  # simulate a long-running computation
        return a + b

    async def handle_click():
        result = await run.cpu_bound(compute_sum, 1, 2)
        ui.notify(f'Sum is {result}')

    # ui.button('Compute', on_click=handle_click)
    # END OF DEMO
    async def mock_click():
        import asyncio
        await asyncio.sleep(1)
        ui.notify('Sum is 3')
    ui.button('Compute', on_click=mock_click)


@doc.demo('Running I/O-bound tasks', '''
    NiceGUI provides an `io_bound` function for running I/O-bound tasks in a separate thread.
    This is useful for long-running I/O operations that would otherwise block the event loop and make the UI unresponsive.
    The function returns a future that can be awaited.
''')
def io_bound_demo():
    import requests

    from nicegui import run

    async def handle_click():
        URL = 'https://httpbin.org/delay/1'
        response = await run.io_bound(requests.get, URL, timeout=3)
        ui.notify(f'Downloaded {len(response.content)} bytes')

    ui.button('Download', on_click=handle_click)


doc.intro(run_javascript_documentation)
doc.intro(clipboard_documentation)


@doc.demo('Events', '''
    You can register coroutines or functions to be called for the following events:

    - `app.on_startup`: called when NiceGUI is started or restarted
    - `app.on_shutdown`: called when NiceGUI is shut down or restarted
    - `app.on_connect`: called for each client which connects (optional argument: nicegui.Client)
    - `app.on_disconnect`: called for each client which disconnects (optional argument: nicegui.Client)
    - `app.on_exception`: called when an exception occurs (optional argument: exception)

    When NiceGUI is shut down or restarted, all tasks still in execution will be automatically canceled.
''')
def lifecycle_demo():
    from datetime import datetime

    from nicegui import app

    # dt = datetime.now()

    def handle_connection():
        global dt
        dt = datetime.now()
    app.on_connect(handle_connection)

    label = ui.label()
    ui.timer(1, lambda: label.set_text(f'Last new connection: {dt:%H:%M:%S}'))
    # END OF DEMO
    global dt
    dt = datetime.now()


@doc.demo('Custom Error Page Handler', '''
    You can register a custom error page handler when the page runs into an error. 
          
    Points aboout the error page handler:
          
    - It must be a synchronous function that takes the error as an argument (expected signature: `def my_error_content(exception):`).
    - Overrides the default "sad face" error page handler, except when the error is re-raised (`raise exception`).
    - Inside the function, you can define the UI elements to be returned to the client, just like in a normal page handler.
    - Return value is ignored.
    - Attached via `app.on_page_exception(my_error_content)`.
          
    The following example shows how to create a custom error page handler that only handles a specific exception.
          
    The default error page handler is still used for all other exceptions.
          
    **Note: Showing the traceback may not be a good idea in production, as it may leak sensitive information.**

''')
def error_page_demo():
    from nicegui import app

    def error_content(exception):
        if not "This is a special exception" in str(exception):
            raise exception
        import traceback
        ui.label('This is a custom error page.')
        ui.label(f'Error: {exception}')
        ui.log().push(traceback.format_exc(chain=False).strip())

    # app.on_page_exception(error_content)

    @ui.page('/raise_special_exception')
    def raise_special_exception():
        raise RuntimeError("This is a special exception")

    @ui.page('/raise_normal_exception')
    def raise_normal_exception():
        raise RuntimeError("This is a normal exception")

    # ui.run()
    # END OF DEMO
    ui.link('Raise special exception', '/raise_special_exception')
    ui.link('Raise normal exception', '/raise_normal_exception')


@doc.demo(app.shutdown)
def shutdown_demo():
    from nicegui import app

    # ui.button('shutdown', on_click=app.shutdown)
    #
    # ui.run(reload=False)
    # END OF DEMO
    ui.button('shutdown', on_click=lambda: ui.notify(
        'Nah. We do not actually shutdown the documentation server. Try it in your own app!'))


doc.intro(storage_documentation)
