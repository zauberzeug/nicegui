from nicegui import ui

from .screen import Screen


def test_leaflet(screen: Screen):
    ui.leaflet()

    screen.open('/')
    assert screen.find_all_by_class('leaflet-pane')
    assert screen.find_all_by_class('leaflet-control-container')
