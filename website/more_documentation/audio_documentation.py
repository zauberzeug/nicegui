from nicegui import ui

from ..documentation_tools import text_demo

def main_demo() -> None:
    a = ui.audio('https://cdn.pixabay.com/download/audio/2022/02/22/audio_d1718ab41b.mp3')
    a.on('ended', lambda _: ui.notify('Audio playback completed'))

    ui.button(on_click=lambda: a.props('muted'), icon='volume_off').props('outline')
    ui.button(on_click=lambda: a.props(remove='muted'), icon='volume_up').props('outline')

url_audio = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
seek_audio = 0

def more() -> None:
    @text_demo('Audio with play/pause/seek controls', '''
        This demo shows how to use play/pause/seek controls.
    ''')
    def control_demo() -> None:
        a = ui.audio(url_audio)
        with ui.row():
            ui.button('Play', on_click=lambda: a.play())
            ui.button('Pause', on_click=lambda: a.pause())
            ui.button('Seek', on_click=lambda: a.seek(seek_audio))
            ui.number("Position", value=seek_audio).bind_value(globals(), 'seek_audio')
