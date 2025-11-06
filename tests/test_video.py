from nicegui import ui
from nicegui.testing import Screen

VIDEO1 = 'https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
VIDEO2 = 'https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4'


def test_replace_video(screen: Screen):
    @ui.page('/')
    def page():
        with ui.row() as container:
            ui.video(VIDEO1)

        def replace():
            container.clear()
            with container:
                ui.video(VIDEO2)
        ui.button('Replace', on_click=replace)

    screen.open('/')
    assert screen.find_by_tag('video').get_attribute('src').endswith('BigBuckBunny.mp4')

    screen.click('Replace')
    screen.wait(0.5)
    assert screen.find_by_tag('video').get_attribute('src').endswith('ElephantsDream.mp4')


def test_change_source(screen: Screen):
    @ui.page('/')
    def page():
        audio = ui.video(VIDEO1)
        ui.button('Change source', on_click=lambda: audio.set_source(VIDEO2))

    screen.open('/')
    assert screen.find_by_tag('video').get_attribute('src').endswith('BigBuckBunny.mp4')

    screen.click('Change source')
    screen.wait(0.5)
    assert screen.find_by_tag('video').get_attribute('src').endswith('ElephantsDream.mp4')
