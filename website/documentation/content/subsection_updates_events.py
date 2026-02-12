from nicegui import ui

from . import (
    doc,
    generic_events_documentation,
    refreshable_documentation,
)

doc.title('Updates & Events')


@doc.demo('UI Updates', '''
    NiceGUI tries to automatically synchronize the state of UI elements with the client,
    e.g. when a label text, an input value or style/classes/props of an element have changed.
    In other cases, you can explicitly call `element.update()` or `ui.update(*elements)` to update.
    The demo code shows how to update a `ui.radio` after a new option is added.
''')
def ui_updates_demo():
    radio = ui.radio(['A', 'B', 'C'])

    ui.button('Add option', on_click=lambda: radio.options.append('D'))
    ui.button('Update', on_click=radio.update)


doc.intro(refreshable_documentation)
doc.intro(generic_events_documentation)


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
    import httpx

    from nicegui import run

    async def handle_click():
        URL = 'https://httpbin.org/delay/1'
        response = await run.io_bound(httpx.get, URL, timeout=3)
        ui.notify(f'Downloaded {len(response.content)} bytes')

    ui.button('Download', on_click=handle_click)
