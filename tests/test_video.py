from nicegui import ui
from nicegui.testing import Screen


def test_replace_video(screen: Screen):
    with ui.row() as container:
        ui.video('https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4')

    def replace():
        container.clear()
        with container:
            ui.video('https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4')
    ui.button('Replace', on_click=replace)

    screen.open('/')
    assert screen.find_by_tag('video').get_attribute('src').endswith('BigBuckBunny.mp4')
    screen.click('Replace')
    screen.wait(0.5)
    assert screen.find_by_tag('video').get_attribute('src').endswith('ElephantsDream.mp4')
