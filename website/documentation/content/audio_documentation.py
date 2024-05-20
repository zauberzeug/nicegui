from nicegui import ui

from . import doc


@doc.demo(ui.audio)
def main_demo() -> None:
    a = ui.audio('https://cdn.pixabay.com/download/audio/2022/02/22/audio_d1718ab41b.mp3')
    a.on('ended', lambda _: ui.notify('Audio playback completed'))

    ui.button(on_click=lambda: a.props('muted'), icon='volume_off').props('outline')
    ui.button(on_click=lambda: a.props(remove='muted'), icon='volume_up').props('outline')


@doc.demo('Control the audio element', '''
    This demo shows how to play, pause and seek programmatically.
''')
def control_demo() -> None:
    a = ui.audio('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3')
    ui.button('Play', on_click=a.play)
    ui.button('Pause', on_click=a.pause)
    ui.button('Jump to 0:30', on_click=lambda: a.seek(30))


@doc.demo('Event subscription', '''
    This demo shows how to subscribe to some of the [available events](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio#events).  
''')
def event_demo() -> None:
    a = ui.audio('https://cdn.pixabay.com/download/audio/2022/02/22/audio_d1718ab41b.mp3')
    a.on('play', lambda _: ui.notify('Started'))
    a.on('pause', lambda _: ui.notify('Paused'))
    a.on('ended', lambda _: ui.notify('Completed'))


doc.reference(ui.audio)
