from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    ui.button('Say hi!', on_click=lambda: ui.notify('Hi!', closeBtn='OK'))


def more() -> None:
    @text_demo('Notification Types', '''
        There are different types that can be used to indicate the nature of the notification.
    ''')
    def notify_colors():
        ui.button('negative', on_click=lambda: ui.notify('error', type='negative'))
        ui.button('positive', on_click=lambda: ui.notify('success', type='positive'))
        ui.button('warning', on_click=lambda: ui.notify('warning', type='warning'))

    @text_demo('Multiline Notifications', '''
        To allow a notification text to span multiple lines, it is sufficient to pass the `mutliLine` keyword with `True`.
        If manual newline breaks are required (e.g. `\n`), you need to define a CSS style and pass it to the notification as shown in the example.
    ''')
    def multiline():
        ui.html('<style>.multi-line-notification { white-space: pre-line; }</style>')
        ui.button('show', on_click=lambda: ui.notify(
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit. \n'
            'Hic quisquam non ad sit assumenda consequuntur esse inventore officia. \n'
            'Corrupti reiciendis impedit vel, '
            'fugit odit quisquam quae porro exercitationem eveniet quasi.',
            multiLine=True,
            classes='multi-line-notification',
        ))
