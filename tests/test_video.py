from nicegui import app, ui
from nicegui.testing import Screen


def _serve_empty_file(path: str):
    @app.get(path)
    def get_empty_file():
        return b''


def test_replace_video(screen: Screen):
    _serve_empty_file(VIDEO1 := '/video1.mp4')
    _serve_empty_file(VIDEO2 := '/video2.mp4')

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
    assert screen.find_by_tag('video').get_attribute('src').endswith(VIDEO1)

    screen.click('Replace')
    screen.wait(0.5)
    assert screen.find_by_tag('video').get_attribute('src').endswith(VIDEO2)


def test_change_source(screen: Screen):
    _serve_empty_file(VIDEO1 := '/video1.mp4')
    _serve_empty_file(VIDEO2 := '/video2.mp4')

    @ui.page('/')
    def page():
        video = ui.video(VIDEO1)
        ui.button('Change source', on_click=lambda: video.set_source(VIDEO2))

    screen.open('/')
    assert screen.find_by_tag('video').get_attribute('src').endswith(VIDEO1)

    screen.click('Change source')
    screen.wait(0.5)
    assert screen.find_by_tag('video').get_attribute('src').endswith(VIDEO2)
