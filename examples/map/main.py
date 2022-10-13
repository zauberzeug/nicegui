#!/usr/bin/env python3
from nicegui import ui

# this module wraps the JavaScript lib leafletjs.com into an easy-to-use NiceGUI element
import leaflet


@ui.page('/')
def main_page():
    map = leaflet.map()
    locations = {
        (52.5200, 13.4049): 'Berlin',
        (40.7306, -74.0060): 'New York',
        (39.9042, 116.4074): 'Beijing',
        (35.6895, 139.6917): 'Tokyo',
    }
    selection = ui.select(locations, on_change=map.set_location).style('width: 10em')
    yield  # all code below is executed after page is ready
    default_location = next(iter(locations))
    # this will trigger the map.set_location event; which is js and must be run after page is ready
    selection.set_value(default_location)


ui.run()
