from nicegui import DistributedEvent, Event, ui

from . import doc


@doc.demo(Event)
def events_demo():
    from nicegui import Event

    tweet = Event[str]()

    # @ui.page('/')
    def page():
        with ui.row(align_items='center'):
            message = ui.input('Tweet')
            ui.button(icon='send', on_click=lambda: tweet.emit(message.value)).props('flat')

        tweet.subscribe(lambda m: ui.notify(f'Someone tweeted: "{m}"'))
    page()  # HIDE


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

    # @ui.page('/')
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
    page()  # HIDE


@doc.demo('Distributed events', '''
    Use `DistributedEvent` to share events across all NiceGUI instances on a network.
    Enable distributed mode with `ui.run(distributed=True)` for Zenoh's defaults,
    `ui.run(distributed=["host1", "host2:7447"])` for an explicit peer list,
    or `ui.run(distributed={...})` to pass a raw Zenoh config dict.

    When enabled, every `DistributedEvent` automatically forwards its emissions to every
    other instance that shares the same `storage_secret` - regular `Event` instances stay
    local. The example below contrasts the two.
''')
def distributed_events():
    from nicegui import DistributedEvent, Event

    shared_event = DistributedEvent[str]()
    local_event = Event[str]()

    # @ui.page('/')
    def page():
        with ui.column():
            ui.label('Distributed event (shared across instances):')
            with ui.row(align_items='center'):
                message = ui.input('Message')
                ui.button('Send to all', on_click=lambda: shared_event.emit(message.value))
            shared_event.subscribe(lambda m: ui.notify(f'Received: "{m}"'))

            ui.separator()
            ui.label('Local event (this instance only):')
            with ui.row(align_items='center'):
                local_msg = ui.input('Local message')
                ui.button('Send locally', on_click=lambda: local_event.emit(local_msg.value))
            local_event.subscribe(lambda m: ui.notify(f'Local: "{m}"', color='orange'))
    page()  # HIDE


doc.reference(Event)
doc.reference(DistributedEvent)
