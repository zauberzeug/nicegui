#!/usr/bin/env python3
from leaflet import leaflet  # this module wraps the JavaScript lib leafletjs.com into an easy-to-use NiceGUI element

from nicegui import Client, ui

locations = {
    (52.5200, 13.4049): 'Berlin',
    (40.7306, -74.0060): 'New York',
    (39.9042, 116.4074): 'Beijing',
    (35.6895, 139.6917): 'Tokyo',
}


@ui.page('/')
async def main_page(client: Client):
    map = leaflet().classes('w-full h-96')
    selection = ui.select(locations, on_change=lambda e: map.set_location(e.value)).classes('w-40')
    await client.connected()  # wait for websocket connection
    selection.set_value(next(iter(locations)))  # trigger map.set_location with first location in selection


ui.run()
