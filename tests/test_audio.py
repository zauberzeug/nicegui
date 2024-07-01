from nicegui import ui
from nicegui.testing import SeleniumScreen

SONG1 = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'
SONG2 = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3'


def test_replace_audio(screen: SeleniumScreen):
    with ui.row() as container:
        ui.audio(SONG1)

    def replace():
        container.clear()
        with container:
            ui.audio(SONG2)
    ui.button('Replace', on_click=replace)

    screen.open('/')
    assert screen.find_by_tag('audio').get_attribute('src').endswith('SoundHelix-Song-1.mp3')
    screen.click('Replace')
    screen.wait(0.5)
    assert screen.find_by_tag('audio').get_attribute('src').endswith('SoundHelix-Song-2.mp3')


def test_change_source(screen: SeleniumScreen):
    audio = ui.audio(SONG1)
    ui.button('Change source', on_click=lambda: audio.set_source(SONG2))

    screen.open('/')
    assert screen.find_by_tag('audio').get_attribute('src').endswith('SoundHelix-Song-1.mp3')
    screen.click('Change source')
    screen.wait(0.5)
    assert screen.find_by_tag('audio').get_attribute('src').endswith('SoundHelix-Song-2.mp3')
