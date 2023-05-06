from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    ui.button('Say hi!', on_click=lambda: ui.notify('Hi!', close_button='OK'))


def more() -> None:
    @text_demo('Notification Types', '''
        There are different types that can be used to indicate the nature of the notification.
    ''')
    def notify_colors():
        ui.button('negative', on_click=lambda: ui.notify('error', type='negative'))
        ui.button('positive', on_click=lambda: ui.notify('success', type='positive'))
        ui.button('warning', on_click=lambda: ui.notify('warning', type='warning'))
