#!/usr/bin/env python3
"""Websockets example showing messages from connected clients and broadcasting via button click.

NOTE: NiceGUI already handles all the communication for you, so you don't need to worry about websockets and the like normally.
This example is only for advanced use cases where you want to allow other, non-NiceGUI clients to connect to your server.
"""
import asyncio

import websockets
from websockets.server import ServerConnection

from nicegui import Event, app, ui

CONNECTIONS: set[ServerConnection] = set()

connections_updated = Event()
message_received = Event()


@ui.page('/')
def page():
    ui.markdown('''
        # Websockets Example

        Run this in the console to connect:
        ```bash
        python -m websockets ws://localhost:8765/
        ```
    ''')
    count = ui.number(value=len(CONNECTIONS), suffix='connections').props('readonly').classes('w-32')
    connections_updated.subscribe(lambda: count.set_value(len(CONNECTIONS)))

    ui.label('Incoming messages:')
    messages = ui.log()
    message_received.subscribe(messages.push)

    ui.button('Send hello', on_click=lambda: websockets.broadcast(CONNECTIONS, 'Hello!'))


@app.on_startup
async def start_websocket_server():
    async with websockets.serve(handle_connect, 'localhost', 8765):
        await asyncio.Future()


async def handle_connect(websocket: ServerConnection):
    """Register the new websocket connection, handle incoming messages and remove the connection when it is closed."""
    try:
        CONNECTIONS.add(websocket)
        connections_updated.emit()
        async for message in websocket:
            message_received.emit(str(message))
    finally:
        CONNECTIONS.remove(websocket)
        connections_updated.emit()

ui.run()
