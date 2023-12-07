from nicegui import ui

from . import doc


@doc.demo(ui.video)
def main_demo() -> None:
    v = ui.video('https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4')
    v.on('ended', lambda _: ui.notify('Video playback completed'))


@doc.demo('Control the video element', '''
    This demo shows how to play, pause and seek programmatically.
''')
def control_demo() -> None:
    v = ui.video('https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4')
    ui.button('Play', on_click=v.play)
    ui.button('Pause', on_click=v.pause)
    ui.button('Jump to 0:05', on_click=lambda: v.seek(5))


doc.reference(ui.video)
