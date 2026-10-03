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
    Using `add_action` you can add action buttons to a notification.

    - The first argument is a callback that is invoked when the action button is clicked.
    - You can set `no_dismiss=True` to prevent the notification from being dismissed when the action is clicked.
    - The `color` parameter accepts Quasar colors, Tailwind colors, or CSS colors.
''')
def notification_with_actions_demo() -> None:
    def spawn_notification():
        n = ui.notification('This is a notification with actions', timeout=None)
        n.add_action(lambda: ui.notify('Dismissed!'), text='Dismiss', color='primary', icon='close')
        n.add_action(lambda: ui.notify('Action 1!'), text='Action 1', color='blue-500', icon='check')
        n.add_action(lambda: ui.notify('Action 2!'), text='Action 2', color='#00ffff', icon='check', no_dismiss=True)
    ui.button('Spawn Notification', on_click=spawn_notification)


doc.reference(ui.notification)
