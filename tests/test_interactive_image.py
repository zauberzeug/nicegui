from pathlib import Path
from typing import List

import pytest
from selenium.webdriver.common.action_chains import ActionChains

from nicegui import app, ui
from nicegui.testing import Screen

URL_PATH1 = '/test1.jpg'
URL_PATH2 = '/test2.jpg'


@pytest.fixture(autouse=True)
def provide_image_files():
    app.add_static_file(local_file=Path(__file__).parent / 'media' / 'test1.jpg', url_path=URL_PATH1)
    app.add_static_file(local_file=Path(__file__).parent / 'media' / 'test2.jpg', url_path=URL_PATH2)


def test_set_source_in_tab(screen: Screen):
    """https://github.com/zauberzeug/nicegui/issues/488"""
    @ui.page('/')
    async def page():
        with ui.tabs() as tabs:
            ui.tab('A')
            ui.tab('B')
        with ui.tab_panels(tabs, value='A'):
            with ui.tab_panel('A'):
                ui.label('Tab A')
                img = ui.interactive_image()
            with ui.tab_panel('B'):
                ui.label('Tab B')
        await ui.context.client.connected()
        img.set_source(URL_PATH1)

    screen.open('/')
    screen.wait(0.5)
    assert screen.find_by_tag('img').get_attribute('src').endswith(URL_PATH1)
    screen.click('B')
    screen.wait(0.5)
    screen.click('A')
    assert screen.find_by_tag('img').get_attribute('src').endswith(URL_PATH1)


@pytest.mark.parametrize('cross', [True, False])
def test_with_cross(screen: Screen, cross: bool):
    ui.interactive_image(URL_PATH1, content='<circle cx="100" cy="100" r="15" />', cross=cross)

    screen.open('/')
    screen.find_by_tag('svg')
    with screen.implicitly_wait(0.5):
        assert len(screen.find_all_by_tag('line')) == (2 if cross else 0)
        assert len(screen.find_all_by_tag('circle')) == 1


def test_replace_interactive_image(screen: Screen):
    with ui.row() as container:
        ui.interactive_image(URL_PATH1)

    def replace():
        container.clear()
        with container:
            ui.interactive_image(URL_PATH2)
    ui.button('Replace', on_click=replace)

    screen.open('/')
    assert (screen.find_by_tag('img').get_attribute('src') or '').endswith(URL_PATH1)
    screen.click('Replace')
    screen.wait(0.5)
    assert (screen.find_by_tag('img').get_attribute('src') or '').endswith(URL_PATH2)


@pytest.mark.parametrize('cross', [True, False])
def test_mousemove_event(screen: Screen, cross: bool):
    counter = {'value': 0}
    ii = ui.interactive_image(URL_PATH1, cross=cross, events=['mousemove'],
                              on_mouse=lambda: counter.update(value=counter['value'] + 1))

    screen.open('/')
    element = screen.find_element(ii)
    ActionChains(screen.selenium) \
        .move_to_element_with_offset(element, 0, 0) \
        .pause(0.5) \
        .move_by_offset(10, 10) \
        .pause(0.5) \
        .perform()
    assert counter['value'] > 0


def test_loaded_event(screen: Screen):
    sources: List[str] = []
    ii = ui.interactive_image(URL_PATH1)
    ii.on('loaded', lambda e: sources.append(e.args['source']))
    ui.button('Change Source', on_click=lambda: ii.set_source(URL_PATH2))

    screen.open('/')
    screen.wait_for(lambda: len(sources) == 1)
    screen.click('Change Source')
    screen.wait_for(lambda: len(sources) == 2)
    assert sources[1].endswith(URL_PATH2)
    assert screen.find_by_tag('img').get_attribute('src') == sources[1]
