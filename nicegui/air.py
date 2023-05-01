import gzip
import logging
from typing import Any, Dict

import httpx
from socketio import AsyncClient

from . import globals
from .nicegui import handle_disconnect, handle_event, handle_handshake, handle_javascript_response

RELAY_HOST = 'http://localhost'


class Air:

    def __init__(self, token: str) -> None:
        self.token = token
        self.relay = AsyncClient()
        self.client = httpx.AsyncClient(app=globals.app, base_url="http://test")

        @self.relay.on('get')
        async def on_get(data: Dict[str, Any]) -> Dict[str, Any]:
            headers = {'Accept-Encoding': 'identity', 'X-Forwarded-Prefix': data['prefix']}
            response = await self.client.get(data['path'], headers=headers)
            content = response.content.replace(
                b'const extraHeaders = {};',
                (f'const extraHeaders = {{ "fly-force-instance-id" : "{data["instance-id"]}" }};').encode(),
            )
            headers = dict(response.headers)
            headers['content-encoding'] = 'gzip'
            compressed = gzip.compress(content)
            headers['content-length'] = str(len(compressed))
            return {
                'status_code': response.status_code,
                'headers': headers,
                'content': compressed,
            }

        @self.relay.on('ready')
        def on_ready(data: Dict[str, Any]) -> None:
            print(f'NiceGUI is on air at {data["device_url"]}', flush=True)

        @self.relay.on('error')
        def on_error(data: Dict[str, Any]) -> None:
            print('Error:', data['message'], flush=True)

        @self.relay.on('handshake')
        def on_handshake(data: Dict[str, Any]) -> bool:
            client_id = data['client_id']
            if client_id not in globals.clients:
                return False
            client = globals.clients[client_id]
            client.environ = data['environ']
            client.on_air = True
            handle_handshake(client)
            return True

        @self.relay.on('client_disconnect')
        def on_disconnect(data: Dict[str, Any]) -> None:
            client_id = data['client_id']
            if client_id not in globals.clients:
                return
            client = globals.clients[client_id]
            handle_disconnect(client)

        @self.relay.on('event')
        def on_event(data: Dict[str, Any]) -> None:
            client_id = data['client_id']
            if client_id not in globals.clients:
                return
            client = globals.clients[client_id]
            if 'socket_id' in data['msg']['args']:
                data['msg']['args']['socket_id'] = client_id  # HACK: translate socket_id of ui.scene's init event
            handle_event(client, data['msg'])

        @self.relay.on('javascript_response')
        def on_javascript_response(data: Dict[str, Any]) -> None:
            client_id = data['client_id']
            if client_id not in globals.clients:
                return
            client = globals.clients[client_id]
            handle_javascript_response(client, data['msg'])

        @self.relay.on('out_of_time')
        async def on_move() -> None:
            print('Sorry, you have reached the time limit of this on-air preview.', flush=True)
            await self.connect()

    async def connect(self) -> None:
        try:
            if self.relay.connected:
                await self.relay.disconnect()
            await self.relay.connect(
                f'{RELAY_HOST}?device_token={self.token}',
                socketio_path='/on_air/socket.io',
                transports=['websocket', 'polling'],
            )
        except:
            logging.exception('Could not connect to NiceGUI on air server.')
            print('Could not connect to NiceGUI on air server.', flush=True)

    async def disconnect(self) -> None:
        await self.relay.disconnect()

    async def emit(self, message_type: str, data: Dict[str, Any], room: str) -> None:
        await self.relay.emit('forward', {'event': message_type, 'data': data, 'room': room})
