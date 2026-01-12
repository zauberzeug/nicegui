import time
from base64 import b64decode
from tempfile import NamedTemporaryFile

import numpy as np
from fastapi import Response
from PIL import Image

from nicegui import app, ui
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


def test_leaflet_unhide(screen: Screen):
    @app.get('/fakeimage')
    def fake_image():
        return Response(content=b64decode('R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs='), media_type='image/gif')

    @ui.page('/')
    def page():
        with ui.card().classes('w-full') as card:
            myleaflet = ui.leaflet(center=(51.505, -0.09)).classes('h-screen')
            ui.run_javascript(f"L.tileLayer('/fakeimage').addTo(getElement({myleaflet.id}).map);")
            card.set_visibility(False)
        ui.button('Show map card', on_click=lambda: card.set_visibility(True))

    def count_gray_pixels() -> int:
        with NamedTemporaryFile(suffix='.png') as tmp_path:
            screen.find_by_tag('body').screenshot(str(tmp_path.name))
            img = Image.open(tmp_path.name)
            return (np.array(img)[:, :, :3] == 0xdd).all(axis=2).sum()

    screen.open('/')
    screen.click('Show map card')
    screen.wait(1)
    assert count_gray_pixels() < 10000
