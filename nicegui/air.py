import gzip
from typing import Any, Dict

from fastapi.testclient import TestClient
from socketio import AsyncClient

from . import globals
from .nicegui import handle_disconnect, handle_event, handle_handshake

RELAY_HOST = 'https://n6.zauberzeug.com'


class Air:

    def __init__(self) -> None:
        self.relay = AsyncClient()
        self.test_client = TestClient(globals.app)

        @self.relay.on('get')
        def on_get(data: Dict[str, Any]) -> Dict[str, Any]:
            headers = headers = {'Accept-Encoding': 'identity', 'X-Forwarded-Prefix': data['prefix']}
            response = self.test_client.get(data['path'], headers=headers)
            return {
                'status_code': response.status_code,
                'headers': {'Content-Encoding': 'gzip'},
                'content': gzip.compress(response.content),
                'media_type': response.headers.get('content-type'),
            }

        @self.relay.on('handshake')
        def on_handshake(data: Dict[str, Any]) -> bool:
            client_id = data['client_id']
            if client_id not in globals.clients:
                return False
            client = globals.clients[client_id]
            client.environ = data['environ']
            handle_handshake(client)
            return True

        @self.relay.on('disconnect')
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
            handle_event(client, data['msg'])

    async def connect(self) -> None:
        await self.relay.connect(RELAY_HOST, socketio_path='/on_air/socket.io')

    async def emit(self, message_type: str, data: Dict[str, Any], room: str) -> None:
        await self.relay.emit('forward', {'event': message_type, 'data': data, 'room': room})
