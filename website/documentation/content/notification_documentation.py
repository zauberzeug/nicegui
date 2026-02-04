from nicegui import ui

from . import doc


@doc.demo(ui.notification)
def main_demo() -> None:
    import asyncio

    async def compute():
        n = ui.notification(timeout=None)
        for i in range(10):
            n.message = f'Computing {i/10:.0%}'
            n.spinner = True
            await asyncio.sleep(0.2)
        n.message = 'Done!'
        n.spinner = False
        await asyncio.sleep(1)
        n.dismiss()

    ui.button('Compute', on_click=compute)


@doc.demo('Notification with Actions', '''
    Using `add_action` you can add buttons to a notification, which trigger an event when clicked.

    - The first argument is the event name, which can be used to listen for the action using the `on` method.
    - It takes the same arguments as `ui.button`, and any more which [Quasar's `q-btn` supports](https://quasar.dev/vue-components/button#props).
      - Notably, `color` can be a Quasar color, a Tailwind color, or a CSS color, just like for `ui.button`.
    - Additionally, you can set `no_dismiss=True` to prevent the notification from being dismissed when the action is clicked.
''')
def notification_with_actions_demo() -> None:
    def spawn_notification():
        n = ui.notification('This is a notification with actions', timeout=None)
        n.add_action('dismiss', text='Dismiss', color='primary', icon='close')
        n.add_action('action1', text='Action 1', color='blue-500', icon='check')
        n.add_action('action2', text='Action 2', color='#00ffff', icon='check', no_dismiss=True)
        n.on('dismiss', lambda: ui.notify('Dismissed!'))
        n.on('action1', js_handler='() => alert("Action 1 clicked!")')
        n.on('action2', lambda: ui.notify('Action 2 clicked!'))
    ui.button('Spawn Notification', on_click=spawn_notification)


doc.reference(ui.notification)
