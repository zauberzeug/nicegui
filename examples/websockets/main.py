#!/usr/bin/env python3
"""Websockets example showing messages from connected clients and broadcasting via button click.

NOTE: NiceGUI already handles all the communication for you, so you don't need to worry about websockets and the like normally.
This example is only for advanced use cases where you want to allow other, non-NiceGUI clients to connect to your server.
"""
import asyncio
from typing import Set

import websockets
from websockets.server import WebSocketServerProtocol

from nicegui import app, ui

CONNECTIONS: Set[WebSocketServerProtocol] = set()

ui.label('Websockets demo').classes('text-2xl')
ui.label('Run this in the console to connect:')
ui.code('python -m websockets ws://localhost:8765/').classes('pr-8 pt-1 h-12')
with ui.row().classes('items-center'):
    connections_label = ui.label('0')
    ui.label('connections')
    ui.button('send hello', on_click=lambda: websockets.broadcast(CONNECTIONS, 'Hello!')).props('flat')
ui.separator().classes('mt-6')
ui.label('incoming messages:')
messages = ui.column().classes('ml-4')


async def handle_connect(websocket: WebSocketServerProtocol):
    """
    Register the new websocket connection, handle incoming messages, and remove the connection when it is closed.

    Parameters:
        websocket (WebSocketServerProtocol): The WebSocket connection object.

    Returns:
        None

    Raises:
        N/A

    Usage:
        This function is used to handle a new websocket connection. It registers the connection, handles incoming
        messages, and removes the connection when it is closed. The function should be called with a valid
        WebSocketServerProtocol object as the `websocket` parameter.
    """
    try:
        CONNECTIONS.add(websocket)
        connections_label.text = len(CONNECTIONS)
        async for data in websocket:
            with messages:
                ui.label(str(data))
    finally:
        CONNECTIONS.remove(websocket)
        connections_label.text = len(CONNECTIONS)


async def start_websocket_server():
    """
    Starts a WebSocket server on the localhost at port 8765.

    This function creates a WebSocket server using the `websockets` library and serves incoming connections
    by calling the `handle_connect` function. It runs asynchronously using the `async with` statement.

    Parameters:
        None

    Returns:
        None

    Usage:
        - Import the `start_websocket_server` function from this module.
        - Call the `start_websocket_server` function to start the WebSocket server.

    Example:
        from main import start_websocket_server

        async def handle_connect(websocket, path):
            # Handle incoming WebSocket connections

        async def main():
            await start_websocket_server()

        asyncio.run(main())
    """
    async with websockets.serve(handle_connect, 'localhost', 8765):
        await asyncio.Future()

# start the websocket server when NiceGUI server starts
app.on_startup(start_websocket_server)

ui.run()
