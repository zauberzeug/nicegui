from nicegui import ui
from website.documentation_tools import text_demo


def main_demo() -> None:
    v = ui.video('https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4')
    v.on('ended', lambda _: ui.notify('Video playback completed'))


def more() -> None:
    @text_demo('Video start position', '''
        This demo shows how to use JavaScript to set the start position of a video.
    ''')
    def advanced_usage() -> None:
        async def set_time(_):
            await ui.run_javascript(f'getElement({v.id}).$el.currentTime = 5;', respond=False)

        v = ui.video('https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4')
        v.on('loadedmetadata', set_time)
