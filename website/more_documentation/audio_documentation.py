from nicegui import ui


def main_demo() -> None:
    a = ui.audio('https://cdn.pixabay.com/download/audio/2022/02/22/audio_d1718ab41b.mp3')
    a.on('ended', lambda _: ui.notify('Audio playback completed'))

    ui.button(on_click=lambda: a.props('muted'), icon='volume_off').props('outline')
    ui.button(on_click=lambda: a.props(remove='muted'), icon='volume_up').props('outline')
