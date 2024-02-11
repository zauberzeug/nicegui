import time

from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_leaflet(screen: SeleniumScreen):
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
