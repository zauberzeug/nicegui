from nicegui import globals, ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    """Generic Events

    Most UI elements come with predefined events.
    For example, a `ui.button` like "A" in the demo has an `on_click` parameter that expects a coroutine or function.
    But you can also use the `on` method to register a generic event handler like for "B".
    This allows you to register handlers for any event that is supported by JavaScript and Quasar.

    For example, you can register a handler for the `mousemove` event like for "C", even though there is no `on_mousemove` parameter for `ui.button`.
    Some events, like `mousemove`, are fired very often.
    To avoid performance issues, you can use the `throttle` parameter to only call the handler every `throttle` seconds ("D").

    The generic event handler can be synchronous or asynchronous and optionally takes an event dictionary as argument ("E").
    You can also specify which attributes of the JavaScript or Quasar event should be passed to the handler ("F").
    This can reduce the amount of data that needs to be transferred between the server and the client.
    """
    with ui.row():
        ui.button('A', on_click=lambda: ui.notify('You clicked the button A.'))
        ui.button('B').on('click', lambda: ui.notify('You clicked the button B.'))
    with ui.row():
        ui.button('C').on('mousemove', lambda: ui.notify('You moved on button C.'))
        ui.button('D').on('mousemove', lambda: ui.notify('You moved on button D.'), throttle=0.5)
    with ui.row():
        ui.button('E').on('mousedown', lambda e: ui.notify(str(e)))
        ui.button('F').on('mousedown', lambda e: ui.notify(str(e)), ['ctrlKey', 'shiftKey'])


def more() -> None:
    @text_demo('Modifiers', '''
        You can also include [key modifiers](https://vuejs.org/guide/essentials/event-handling.html#key-modifiers>) (shown in input "A"),
        modifier combinations (shown in input "B"),
        and [event modifiers](https://vuejs.org/guide/essentials/event-handling.html#mouse-button-modifiers>) (shown in input "C").
    ''')
    def modifiers() -> None:
        with ui.row():
            ui.input('A').classes('w-12').on('keydown.space', lambda: ui.notify('You pressed space.'))
            ui.input('B').classes('w-12').on('keydown.y.shift', lambda: ui.notify('You pressed Shift+Y'))
            ui.input('C').classes('w-12').on('keydown.once', lambda: ui.notify('You started typing.'))

    @text_demo('Custom events', '''
        It is fairly easy to emit custom events from JavaScript which can be listened to with `element.on(...)`.
        This can be useful if you want to call Python code when something happens in JavaScript.
        In this example we are listening to the `visibilitychange` event of the browser tab.
    ''')
    async def custom_events() -> None:
        tabwatch = ui.checkbox('Watch browser tab re-entering') \
            .on('tabvisible', lambda: ui.notify('welcome back') if tabwatch.value else None)
        ui.add_head_html(f'''
            <script>
            document.addEventListener('visibilitychange', () => {{
                if (document.visibilityState === 'visible')
                    document.getElementById({tabwatch.id}).dispatchEvent(new CustomEvent('tabvisible'));
            }});
            </script>
        ''')
        # END OF DEMO
        await globals.get_client().connected()
        await ui.run_javascript(f'''
            document.addEventListener('visibilitychange', () => {{
                if (document.visibilityState === 'visible')
                    document.getElementById({tabwatch.id}).dispatchEvent(new CustomEvent('tabvisible'));
            }});
        ''', respond=False)
