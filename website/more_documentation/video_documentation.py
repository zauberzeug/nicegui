from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    v = ui.video('https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4')
    v.on('ended', lambda _: ui.notify('Video playback completed'))


def more() -> None:
    @text_demo('Video start position', '''
        This demo shows how to set the start position of a video.
    ''')
    def start_position_demo() -> None:
        v = ui.video('https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4')
        v.on('loadedmetadata', lambda: v.seek(5))
