#!/usr/bin/env python3

from nicegui import ui

# this module wraps the javascript lib leafletjs.com into an easy to use NiceGUI element
import leaflet

locations = {
    (52.5200, 13.4049): 'Berlin',
    (40.7306, -74.0060): 'New York',
    (39.9042, 116.4074): 'Beijing',
    (35.6895, 139.6917): 'Tokyo',
}
selection = None


@ui.page('/', on_page_ready=lambda: selection.set_value(next(iter(locations))))
def main_page():
    # NOTE we need to use the on_page_ready event to make sure the page is loaded before we execute javascript
    global selection
    map = leaflet.map()
    selection = ui.select(locations, on_change=map.set_location).style('width: 10em')


ui.run()
