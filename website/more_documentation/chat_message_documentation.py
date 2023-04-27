from nicegui import ui


def main_demo() -> None:
    name = 'Me'
    ui.chat_message(
        'Hello NiceGUI!', name=name, stamp='now',
        avatar=f'https://robohash.org/{name}?bgset=bg2'
    )
