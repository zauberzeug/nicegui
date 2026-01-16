from nicegui import app, ui

from . import (
    clipboard_documentation,
    doc,
    event_documentation,
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
    The demo code shows how to update a `ui.radio` after a new option is added.
''')
def ui_updates_demo():
    radio = ui.radio(['A', 'B', 'C'])

    ui.button('Add option', on_click=lambda: radio.options.append('D'))
    ui.button('Update', on_click=radio.update)


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
    import httpx

    from nicegui import run

    async def handle_click():
        URL = 'https://httpbin.org/delay/1'
        response = await run.io_bound(httpx.get, URL, timeout=3)
        ui.notify(f'Downloaded {len(response.content)} bytes')

    ui.button('Download', on_click=handle_click)


doc.intro(run_javascript_documentation)
doc.intro(clipboard_documentation)
doc.intro(event_documentation)

doc.text('Error handling', '''
    There are 3 error handling means in NiceGUI:

    1. [`app.on_exception`](#lifecycle_events): Global exception handler
        - Works for all exceptions in the NiceGUI app.
        - Applied app-wide.
        - Handler has no UI context (cannot use `ui.*`).
        - Common sources: `app.timer`, `background_tasks.create`, `run.io_bound`, `run.cpu_bound`.
    2. [`@app.on_page_exception`](#custom_error_page): Custom error page for critical exceptions
        - Works for UI-context exceptions raised **before** the Python-side client is ready.
        - Applied app-wide.
        - Handler may use UI elements but in a new client.
        - Common sources: sync `@ui.page` functions, exceptions in async `@ui.page` functions before `await ui.context.client.connected()`.
    3. [`ui.on_exception`](#ui_on_exception): Page exception handler for non-critical exceptions
        - Works for UI-context exceptions raised **after** the Python-side client is ready.
        - Applied per-page.
        - Handler may use UI elements with the original client at `ui.context.client`.
        - Common sources: `ui.button(on_click=...)`, `ui.timer`, exceptions in async `@ui.page` functions after `await ui.context.client.connected()`

    When an exception occurs:

    - All will be logged via `app.on_exception` (1)
    - UI-context exceptions go to _either_, but never both:
        - `@app.on_page_exception` (2) if raised before client connection
        - `ui.on_exception` (3) if raised after client connection
''')


@doc.demo('Lifecycle events', '''
    You can register coroutines or functions to be called for the following lifecycle events:

    - `app.on_startup`: called when NiceGUI is started or restarted
    - `app.on_shutdown`: called when NiceGUI is shut down or restarted
    - `app.on_connect`: called for each client which connects (even when reconnecting, optional argument: `nicegui.Client`)
    - `app.on_disconnect`: called for each client which disconnects (even when reconnecting, optional argument: `nicegui.Client`, *changed in version 3.0.0*)
    - `app.on_delete`: called when a client is deleted (if it does not reconnect, optional argument: `nicegui.Client`, *added in version 3.0.0*)
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


@doc.auto_execute
@doc.demo('Custom error page', '''
    You can use `@app.on_page_exception` to define a custom error page.

    The handler must be a synchronous function that creates a page like a normal page function.
    It can take the exception as an argument, but it is not required.
    It overrides the default "sad face" error page, except when the error is re-raised.

    The following example shows how to create a custom error page handler that only handles a specific exception.
    The default error page handler is still used for all other exceptions.

    Note: Showing the traceback may not be a good idea in production, as it may leak sensitive information.

    *Added in version 2.20.0*
''')
def error_page_demo():
    from nicegui import app
    import traceback

    @app.on_page_exception
    def timeout_error_page(exception: Exception) -> None:
        if not isinstance(exception, TimeoutError):
            raise exception
        with ui.column().classes('absolute-center items-center gap-8'):
            ui.icon('sym_o_timer', size='xl')
            ui.label(f'{exception}').classes('text-2xl')
            ui.code(traceback.format_exc(chain=False))

    @ui.page('/raise_timeout_error')
    def raise_timeout_error():
        raise TimeoutError('This took too long')

    @ui.page('/raise_runtime_error')
    def raise_runtime_error():
        raise RuntimeError('Something is wrong')

    # @ui.page('/')
    def page():
        ui.link('Raise timeout error (custom error page)', '/raise_timeout_error')
        ui.link('Raise runtime error (default error page)', '/raise_runtime_error')
    page()  # HIDE


@doc.auto_execute
@doc.demo('ui.on_exception', '''
    You can register callback functions using `ui.on_exception` to handle errors
    that occur after the HTML response has been sent to the client.
    This allows you to show a notification or dialog with the error details.
    The following example shows how to create a dialog that displays the error details when an error occurs.

    *Added in version 3.6.0*
''')
def error_event_demo():
    import asyncio
    import traceback

    @ui.page('/error_dialog_page')
    async def error_dialog_page():
        with ui.page_sticky(x_offset=16, y_offset=16):
            fab_error = ui.button(icon='error', color='negative').props('fab')
            fab_error.set_visibility(False)

        def show_error_dialog(error):
            with ui.dialog() as error_dialog, ui.card():
                render_error_details(error, 'max-w-[calc(560px-2rem)]')
                ui.button('Close', on_click=error_dialog.close)
            fab_error.on('click', error_dialog.open).set_visibility(True)

        ui.on_exception(lambda e: show_error_dialog(e.args))
        ui.label('This @ui.page errors out post-HTML-response in 3 seconds')
        await ui.context.client.connected()
        await asyncio.sleep(3)
        raise ValueError('Test exception handling')

    @ui.page('/clear_content_page')
    async def clear_content_page():
        # def clear_content_and_show_error(error):
        #     with ui.context.client.content.clear():
        #         render_error_details(error, 'w-full')
        #         ui.link('Back to menu', '/')

        # ui.on_exception(lambda e: clear_content_and_show_error(e.args))
        # ui.label('This @ui.page errors out post-HTML-response in 3 seconds')
        # await ui.context.client.connected()
        # await asyncio.sleep(3)
        # raise ValueError('Test exception handling')
        with ui.column() as fake_column:  # HIDE
            ui.label('This @ui.page errors out post-HTML-response in 3 seconds')  # HIDE
            await ui.context.client.connected()  # HIDE
            await asyncio.sleep(3)  # HIDE
            fake_column.clear()  # HIDE
            try:  # HIDE
                raise ValueError('Test exception handling')  # HIDE
            except Exception as e:  # HIDE
                render_error_details(e, 'w-full')  # HIDE
            ui.link('Back to menu', '/documentation/section_action_events#error_event')  # HIDE

    def render_error_details(error, code_classes=''):
        ui.label('Page error').classes('text-lg font-bold')
        ui.label(f'{error} ({type(error).__name__})').classes('text-red-600')
        # ui.code(traceback.format_exc(chain=False)).classes(code_classes)
        ui.code(traceback.format_exc(chain=False).replace('# HIDE', '')).classes(code_classes)  # HIDE

    # @ui.page('/')
    def page():
        ui.link('@ui.page raises error, shows error dialog', '/error_dialog_page')
        ui.link('@ui.page raises error, clears the body and shows the error', '/clear_content_page')
    page()  # HIDE


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
