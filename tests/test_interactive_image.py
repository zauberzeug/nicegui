from typing import List

import pytest
from selenium.webdriver.common.action_chains import ActionChains

from nicegui import Client, ui
from nicegui.testing import Screen


def test_set_source_in_tab(screen: Screen):
    """https://github.com/zauberzeug/nicegui/issues/488"""
    @ui.page('/')
    async def page(client: Client):
        with ui.tabs() as tabs:
            ui.tab('A')
            ui.tab('B')
        with ui.tab_panels(tabs, value='A'):
            with ui.tab_panel('A'):
                ui.label('Tab A')
                img = ui.interactive_image()
            with ui.tab_panel('B'):
                ui.label('Tab B')
        await client.connected()
        img.set_source('https://nicegui.io/logo.png')

    screen.open('/')
    screen.wait(0.5)
    assert screen.find_by_tag('img').get_attribute('src') == 'https://nicegui.io/logo.png'
    screen.click('B')
    screen.wait(0.5)
    screen.click('A')
    assert screen.find_by_tag('img').get_attribute('src') == 'https://nicegui.io/logo.png'


@pytest.mark.parametrize('cross, number_of_lines', [(True, 2), (False, 0)])
def test_with_cross(screen: Screen, cross: bool, number_of_lines: int):
    ii = ui.interactive_image('https://nicegui.io/logo.png', cross=cross)
    ii.content = '<circle cx="100" cy="100" r="15" fill="none" stroke="red" stroke-width="4" />'

    screen.open('/')
    screen.wait(0.5)
    screen.find_by_tag('svg')
    with screen.implicitly_wait(0.5):
        assert len(screen.find_all_by_tag('line')) == number_of_lines
        assert len(screen.find_all_by_tag('circle')) == 1


def test_replace_interactive_image(screen: Screen):
    with ui.row() as container:
        ui.interactive_image('https://picsum.photos/id/29/640/360')

    def replace():
        container.clear()
        with container:
            ui.interactive_image('https://picsum.photos/id/30/640/360')
    ui.button('Replace', on_click=replace)

    screen.open('/')
    screen.wait(0.5)
    assert screen.find_by_tag('img').get_attribute('src').endswith('id/29/640/360')
    screen.click('Replace')
    screen.wait(0.5)
    assert screen.find_by_tag('img').get_attribute('src').endswith('id/30/640/360')


@pytest.mark.parametrize('cross', [True, False])
def test_mousemove_event(screen: Screen, cross: bool):
    counter = {'value': 0}
    ii = ui.interactive_image('https://picsum.photos/id/29/640/360', cross=cross, events=['mousemove'],
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
    ii = ui.interactive_image('https://picsum.photos/id/29/640/360')
    ii.on('loaded', lambda e: sources.append(e.args['source']))
    ui.button('Change Source', on_click=lambda: ii.set_source('https://picsum.photos/id/30/640/360'))

    screen.open('/')
    screen.wait(0.5)
    assert len(sources) == 1
    screen.click('Change Source')
    screen.wait(1.5)
    assert len(sources) == 2
    assert sources[1].endswith('id/30/640/360')
    assert screen.find_by_tag('img').get_attribute('src') == sources[1]
