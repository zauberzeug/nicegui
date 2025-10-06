from nicegui import ui, Event

from . import doc


@doc.demo(Event)
def events_demo():
    from nicegui import Event

    tweet = Event[str]()

    @ui.page('/')
    def page():
        with ui.row(align_items='center'):
            message = ui.input('Tweet')
            ui.button(icon='send', on_click=lambda: tweet.emit(message.value)).props('flat')

        tweet.subscribe(lambda m: ui.notify(f'Someone tweeted: "{m}"'))


@doc.demo('Emitting vs. calling events', '''
    The `emit` method fires the event without waiting for the subscribed callbacks to complete.
    If you want to wait for the subscribed callbacks to complete, use the `call` method.

    The following demo shows how to use `call` to reset the button state after the event has been called.

    Note that in this particular case, `submit` could also call `backup` directly.
    But in some situations an event can help to decouple the code.
''')
def emitting_vs_calling_events():
    from nicegui import Event
    import asyncio

    data_submitted = Event[str]()

    @data_submitted.subscribe
    async def backup(data: str):
        print(f'Saving "{data}"...')
        await asyncio.sleep(1)  # simulate writing to database

    @ui.page('/')
    def page():
        async def submit():
            button.disable()
            try:
                await data_submitted.call(data.value)
                data.value = None
            except Exception as e:
                ui.notify(f'Error: {e}', color='negative')
            finally:
                button.enable()

        with ui.row(align_items='center'):
            data = ui.input('Data')
            button = ui.button('Submit', on_click=submit).props('flat')


doc.reference(Event)
