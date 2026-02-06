import base64
import time

from fastapi import Response

from nicegui import app, ui
from nicegui.testing import SharedScreen


def test_leaflet(shared_screen: SharedScreen):
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

    shared_screen.open('/')
    assert shared_screen.find_all_by_class('leaflet-pane')
    assert shared_screen.find_all_by_class('leaflet-control-container')

    deadline = time.time() + 3
    while not m.is_initialized and time.time() < deadline:
        shared_screen.wait(0.1)
    shared_screen.should_contain('Center: 51.505, -0.090')
    shared_screen.should_contain('Zoom: 13')

    shared_screen.click('Zoom in')
    shared_screen.should_contain('Zoom: 14')

    shared_screen.click('Zoom out')
    shared_screen.should_contain('Zoom: 13')

    shared_screen.click('Berlin')
    shared_screen.should_contain('Center: 52.520, 13.405')

    shared_screen.click('London')
    shared_screen.should_contain('Center: 51.505, -0.090')


def test_leaflet_unhide(shared_screen: SharedScreen):
    requested_tiles = set()

    @app.get('/mock_tile/{z}/{x}/{y}')
    def mock_tile(z: str, x: str, y: str) -> Response:
        requested_tiles.add((z, x, y))
        return Response(base64.b64decode('R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs='))

    @ui.page('/')
    def page():
        with ui.card().classes('w-full h-64') as card:
            ui.leaflet().wms_layer(url_template='/mock_tile/{{z}}/{{x}}/{{y}}')
            card.visible = False
        ui.button('Show map card', on_click=lambda: card.set_visibility(True))

    shared_screen.open('/')
    shared_screen.click('Show map card')
    shared_screen.wait(0.5)
    assert len(requested_tiles) == 8
