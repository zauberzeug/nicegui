from nicegui import ui


def main_demo() -> None:
    ui.chat_message('Hello NiceGUI!',
                    name='Robot',
                    stamp='now',
                    avatar='https://robohash.org/ui')
