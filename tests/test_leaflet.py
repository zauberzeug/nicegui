import time
from tempfile import NamedTemporaryFile

from PIL import Image

from nicegui import ui
from nicegui.testing import Screen


def test_leaflet(screen: Screen):
    m = None

    @ui.page('/')
    def page():
        nonlocal m
        m = ui.leaflet(center=(51.505, -0.09), zoom=13)
        ui.label().bind_text_from(m, 'center', lambda center: f'Center: {center[0]:.3f}, {center[1]:.3f}')
        ui.label().bind_text_from(m, 'zoom', lambda zoom: f'Zoom: {zoom}')

        ui.button('Zoom in', on_click=lambda: m.set_zoom(m.zoom + 1))
        ui.button('Zoom out', on_click=lambda: m.set_zoom(m.zoom - 1))

        ui.button('Berlin', on_click=lambda: m.set_center((52.520, 13.405)))
        ui.button('London', on_click=lambda: m.set_center((51.505, -0.090)))

    screen.open('/')
    assert screen.find_all_by_class('leaflet-pane')
    assert screen.find_all_by_class('leaflet-control-container')

    deadline = time.time() + 3
    while not m.is_initialized and time.time() < deadline:
        screen.wait(0.1)
    screen.should_contain('Center: 51.505, -0.090')
    screen.should_contain('Zoom: 13')

    screen.click('Zoom in')
    screen.should_contain('Zoom: 14')

    screen.click('Zoom out')
    screen.should_contain('Zoom: 13')

    screen.click('Berlin')
    screen.should_contain('Center: 52.520, 13.405')

    screen.click('London')
    screen.should_contain('Center: 51.505, -0.090')


def _check_gray_sum(screen: Screen):
    with NamedTemporaryFile(suffix='.png') as tmp_path:
        screen.find_by_tag('body').screenshot(str(tmp_path.name))
        img = Image.open(tmp_path.name)

    # how many of them are Leaflet's gray (#ddd = #dddddd)
    gray_sum = 0
    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):
            r, g, b = pixels[x, y][:3]
            if r == g == b == 0xdd:
                gray_sum += 1
    return gray_sum


def test_leaflet_unhide(screen: Screen):
    @ui.page('/')
    def page():
        onoff2 = ui.switch('Toggle Visibility', value=False)

        with ui.card().classes('w-full').bind_visibility_from(onoff2, 'value'):
            ui.leaflet(center=(51.505, -0.09)).classes('h-screen')

    screen.open('/')
    assert _check_gray_sum(screen) < 10
    screen.click('Toggle Visibility')
    screen.wait(1)
    assert _check_gray_sum(screen) < 10000
