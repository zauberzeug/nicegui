import asyncio
import io
import struct
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from fastapi.responses import StreamingResponse
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains

from nicegui import app, ui
from nicegui.testing import Screen

URL_PATH1 = '/test1.jpg'
URL_PATH2 = '/test2.jpg'


@pytest.fixture(autouse=True)
def provide_image_files(nicegui_reset_globals):
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
    @ui.page('/')
    def page():
        ui.interactive_image(URL_PATH1, content='<circle cx="100" cy="100" r="15" />', cross=cross, sanitize=False)

    screen.open('/')
    screen.find_by_tag('svg')
    with screen.implicitly_wait(0.5):
        assert len(screen.find_all_by_tag('line')) == (2 if cross else 0)
        assert len(screen.find_all_by_tag('circle')) == 1


def test_replace_interactive_image(screen: Screen):
    @ui.page('/')
    def page():
        with ui.row() as container:
            ui.interactive_image(URL_PATH1)

        def replace():
            with container.clear():
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
    ii = None

    @ui.page('/')
    def page():
        nonlocal ii
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
    @ui.page('/')
    def page():
        ii = ui.interactive_image(URL_PATH1)
        ii.on('loaded', lambda: ui.label('loaded'))
        ui.button('Change Source', on_click=lambda: ii.set_source(URL_PATH2))

    screen.open('/')
    screen.click('Change Source')
    screen.should_contain('loaded')
    assert (screen.find_by_tag('img').get_attribute('src') or '').endswith(URL_PATH2)


def test_add_layer(screen: Screen):
    @ui.page('/')
    def page():
        ii = ui.interactive_image(
            URL_PATH1, content='<rect x="0" y="0" width="100" height="100" fill="red" />', sanitize=False)
        ii.add_layer(content='<circle cx="100" cy="100" r="15" />')

    screen.open('/')
    screen.find_by_tag('svg')
    with screen.implicitly_wait(0.5):
        assert len(screen.find_all_by_tag('rect')) == 1
        assert len(screen.find_all_by_tag('circle')) == 1


def test_resync_on_stream_resolution_change(screen: Screen):
    """https://github.com/zauberzeug/nicegui/issues/6122"""
    def jpeg(width: int, height: int) -> bytes:
        buffer = io.BytesIO()
        Image.new('RGB', (width, height)).save(buffer, format='JPEG')
        data = buffer.getvalue()
        # pad to force instant paint
        return data[:2] + b'\xff\xfe' + struct.pack('>H', 40_002) + b' ' * 40_000 + data[2:]

    frame = {'data': jpeg(300, 200)}
    clicks = []

    async def generate() -> AsyncGenerator[bytes, None]:
        for _ in range(600):
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame['data'] + b'\r\n'
            await asyncio.sleep(0.05)

    @app.get('/stream')
    def stream():
        return StreamingResponse(generate(), media_type='multipart/x-mixed-replace; boundary=frame')

    @ui.page('/')
    def page():
        ui.interactive_image('/stream', events=['mousedown'], on_mouse=lambda e: clicks.append((e.image_x, e.image_y)))
        ui.button('Change', on_click=lambda: frame.update(data=jpeg(600, 400)))

    screen.open('/')

    def click_when_width(width: int):
        for _ in range(100):
            if screen.selenium.execute_script('return document.querySelector("img").naturalWidth') == width:
                break
            screen.wait(0.1)
        ActionChains(screen.selenium).move_to_element(screen.find_by_tag('img')).click().perform()
        screen.wait(0.5)
        return clicks[-1]

    assert click_when_width(300) == pytest.approx((150, 100), abs=2)
    screen.click('Change')  # the <img> resolution changes in place, without firing a new "load" event
    assert click_when_width(600) == pytest.approx((300, 200), abs=2)


def test_xss_sanitization(screen: Screen):
    @ui.page('/')
    def page():
        ui.interactive_image(size=(100, 100), content='<rect width="100" height="100" onclick="alert(\'XSS\')" />')

    screen.open('/')
    assert screen.find_all_by_tag('rect')[0].get_attribute('onclick') is None
