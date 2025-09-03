from nicegui import ui

from . import doc

doc.title('Events')


@doc.demo('Subscribing to events', '''
    Events are a powerful tool distribute information between different parts of your code.
    The following demo shows how to define an event, subscribe a callback and emit it.

    Handlers can be synchronous or asynchronous.
    They can also take arguments if the event contains arguments.
''')
def events_demo():
    from nicegui import Event

    click = Event()
    click.subscribe(lambda: ui.notify('clicked'))

    ui.button('Click me', on_click=click.emit)


@doc.demo('Events with arguments', '''
    Events can also include arguments.
    The callback can use them, but also ignore them if they are not needed.
''')
def events_with_arguments():
    from nicegui import Event

    answer = Event[int]()
    answer.subscribe(lambda: ui.notify('Answer found!'))
    answer.subscribe(lambda x: ui.notify(f'{x = }'))

    ui.button('Answer', on_click=lambda: answer.emit(42))


@doc.demo('Emitting vs. calling events', '''
    The `emit` method fires the event without waiting for the subscribed callbacks to complete.
    If you want to wait for the subscribed callbacks to complete, use the `call` method.

    The following demo shows how to use `call` to reset the button state after the event has been called.
''')
def emitting_vs_calling_events():
    import asyncio
    from nicegui import Event

    click = Event()

    @click.subscribe
    async def handler():
        n = ui.notification('Running...')
        await asyncio.sleep(1)
        n.message = 'Done!'

    async def handle_click():
        button.disable()
        await click.call()
        button.enable()

    button = ui.button('Click me', on_click=handle_click)
