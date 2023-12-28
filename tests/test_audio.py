from nicegui import ui
from nicegui.testing import Screen


def test_replace_audio(screen: Screen):
    with ui.row() as container:
        ui.audio('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3')

    def replace():
        container.clear()
        with container:
            ui.audio('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3')
    ui.button('Replace', on_click=replace)

    screen.open('/')
    assert screen.find_by_tag('audio').get_attribute('src').endswith('SoundHelix-Song-1.mp3')
    screen.click('Replace')
    screen.wait(0.5)
    assert screen.find_by_tag('audio').get_attribute('src').endswith('SoundHelix-Song-2.mp3')
