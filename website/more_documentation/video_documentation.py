from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    v = ui.video('https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4')
    v.on('ended', lambda _: ui.notify('Video playback completed'))

url_video = "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4"
seek_video = 0

def more() -> None:
    @text_demo('Video with play/pause/seek controls', '''
        This demo shows how to use play/pause/seek controls.
    ''')
    def control_demo() -> None:
        v = ui.video(url_video)
        with ui.row():
            ui.button('Play', on_click=lambda: v.play())
            ui.button('Pause', on_click=lambda: v.pause())
            ui.button('Seek', on_click=lambda: v.seek(seek_video))
            ui.number("Position", value=seek_video).bind_value(globals(), 'seek_video')

