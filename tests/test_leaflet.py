import base64
import time
from pathlib import Path

from fastapi import Response

from nicegui import app, ui
from nicegui.testing import Screen


def test_leaflet_draw_circle_resize_no_strict_mode_error():
    """Verify that the leaflet-draw patch declares 'var radius' (fix for ReferenceError in strict mode)."""
    patch_file = Path(__file__).parent.parent / 'nicegui' / 'elements' / 'leaflet' / 'patches' / 'leaflet-draw+1.0.4.patch'
    content = patch_file.read_text()
    assert '+\t\tvar radius;' in content, \
        "leaflet-draw patch is missing 'var radius' declaration — strict mode will throw ReferenceError"


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


def test_leaflet_unhide(screen: Screen):
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

    screen.open('/')
    screen.click('Show map card')
    screen.wait(0.5)
    assert len(requested_tiles) == 8
