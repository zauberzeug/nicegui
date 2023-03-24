from nicegui import ui


def main_demo() -> None:
    v = ui.video('https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4')
    v.on('ended', lambda _: ui.notify('Video playback completed'))
