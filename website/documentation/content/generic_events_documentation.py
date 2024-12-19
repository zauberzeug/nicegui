from nicegui import ui

from . import doc

doc.title('Generic Events')


@doc.demo('Generic Events', '''
    Most UI elements come with predefined events.
    For example, a `ui.button` like "A" in the demo has an `on_click` parameter that expects a coroutine or function.
    But you can also use the `on` method to register a generic event handler like for "B".
    This allows you to register handlers for any event that is supported by JavaScript and Quasar.

    For example, you can register a handler for the `mousemove` event like for "C", even though there is no `on_mousemove` parameter for `ui.button`.
    Some events, like `mousemove`, are fired very often.
    To avoid performance issues, you can use the `throttle` parameter to only call the handler every `throttle` seconds ("D").

    The generic event handler can be synchronous or asynchronous and optionally takes `GenericEventArguments` as argument ("E").
    You can also specify which attributes of the JavaScript or Quasar event should be passed to the handler ("F").
    This can reduce the amount of data that needs to be transferred between the server and the client.

    Here you can find more information about the events that are supported:

    - <https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement#events> for HTML elements
    - <https://quasar.dev/vue-components> for Quasar-based elements (see the "Events" tab on the individual component page)
''')
def generic_events_demo() -> None:
    with ui.row():
        ui.button('A', on_click=lambda: ui.notify('You clicked the button A.'))
        ui.button('B').on('click', lambda: ui.notify('You clicked the button B.'))
    with ui.row():
        ui.button('C').on('mousemove', lambda: ui.notify('You moved on button C.'))
        ui.button('D').on('mousemove', lambda: ui.notify('You moved on button D.'), throttle=0.5)
    with ui.row():
        ui.button('E').on('mousedown', lambda e: ui.notify(e))
        ui.button('F').on('mousedown', lambda e: ui.notify(e), ['ctrlKey', 'shiftKey'])


@doc.demo('Specifying event attributes', '''
    **A list of strings** names the attributes of the JavaScript event object:
    ```py
    ui.button().on('click', handle_click, ['clientX', 'clientY'])
    ```

    **An empty list** requests _no_ attributes:
    ```py
    ui.button().on('click', handle_click, [])
    ```

    **The value `None`** represents _all_ attributes (the default):
    ```py
    ui.button().on('click', handle_click, None)
    ```

    **If the event is called with multiple arguments** like QTable's "row-click" `(evt, row, index) => void`,
    you can define a list of argument definitions:
    ```py
    ui.table(...).on('rowClick', handle_click, [[], ['name'], None])
    ```
    In this example the "row-click" event will omit all arguments of the first `evt` argument,
    send only the "name" attribute of the `row` argument and send the full `index`.

    If the retrieved list of event arguments has length 1, the argument is automatically unpacked.
    So you can write
    ```py
    ui.button().on('click', lambda e: print(e.args['clientX'], flush=True))
    ```
    instead of
    ```py
    ui.button().on('click', lambda e: print(e.args[0]['clientX'], flush=True))
    ```

    Note that by default all JSON-serializable attributes of all arguments are sent.
    This is to simplify registering for new events and discovering their attributes.
    If bandwidth is an issue, the arguments should be limited to what is actually needed on the server.
''')
def event_attributes() -> None:
    columns = [
        {'name': 'name', 'label': 'Name', 'field': 'name'},
        {'name': 'age', 'label': 'Age', 'field': 'age'},
    ]
    rows = [
        {'name': 'Alice', 'age': 42},
        {'name': 'Bob', 'age': 23},
    ]
    ui.table(columns=columns, rows=rows, row_key='name') \
        .on('rowClick', ui.notify, [[], ['name'], None])


@doc.demo('Modifiers', '''
    You can also include [key modifiers](https://vuejs.org/guide/essentials/event-handling.html#key-modifiers>) (shown in input "A"),
    modifier combinations (shown in input "B"),
    and [event modifiers](https://vuejs.org/guide/essentials/event-handling.html#mouse-button-modifiers>) (shown in input "C").
''')
def modifiers() -> None:
    with ui.row():
        ui.input('A').classes('w-12').on('keydown.space', lambda: ui.notify('You pressed space.'))
        ui.input('B').classes('w-12').on('keydown.y.shift', lambda: ui.notify('You pressed Shift+Y'))
        ui.input('C').classes('w-12').on('keydown.once', lambda: ui.notify('You started typing.'))


@doc.demo('Custom events', '''
    It is fairly easy to emit custom events from JavaScript with `emitEvent(...)` which can be listened to with `ui.on(...)`.
    This can be useful if you want to call Python code when something happens in JavaScript.
    In this example we are listening to the `visibilitychange` event of the browser tab.
''')
async def custom_events() -> None:
    tabwatch = ui.checkbox('Watch browser tab re-entering')
    ui.on('tabvisible', lambda: ui.notify('Welcome back!') if tabwatch.value else None)
    # ui.add_head_html('''
    #     <script>
    #     document.addEventListener('visibilitychange', () => {
    #         if (document.visibilityState === 'visible') {
    #             emitEvent('tabvisible');
    #         }
    #     });
    #     </script>
    # ''')
    # END OF DEMO
    await ui.context.client.connected()
    ui.run_javascript('''
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                emitEvent('tabvisible');
            }
        });
    ''')


@doc.demo('Pure JavaScript events', '''
    You can also use the `on` method to register a pure JavaScript event handler.
    This can be useful if you want to call JavaScript code without sending any data to the server.
    In this example we are using the `navigator.clipboard` API to copy a string to the clipboard.
''')
def pure_javascript() -> None:
    ui.button('Copy to clipboard') \
        .on('click', js_handler='''() => {
            navigator.clipboard.writeText("Hello, NiceGUI!");
        }''')
