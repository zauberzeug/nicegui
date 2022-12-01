#!/usr/bin/env python3
import leaflet  # this module wraps the JavaScript lib leafletjs.com into an easy-to-use NiceGUI element

from nicegui import Client, ui
from nicegui.events import ValueChangeEventArguments


@ui.page('/')
async def main_page(client: Client):
    map = leaflet.map()
    locations = {
        (52.5200, 13.4049): 'Berlin',
        (40.7306, -74.0060): 'New York',
        (39.9042, 116.4074): 'Beijing',
        (35.6895, 139.6917): 'Tokyo',
    }

    async def handle_location_change(e: ValueChangeEventArguments) -> None:
        with e.client:
            await map.set_location(e.value)
    selection = ui.select(locations, on_change=handle_location_change).style('width: 10em')
    await client.handshake()  # all code below is executed after client is connected
    default_location = next(iter(locations))
    # this will trigger the map.set_location event; which is js and must be run after client has connected
    selection.set_value(default_location)


ui.run()
