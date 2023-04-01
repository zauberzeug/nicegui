import gzip
from typing import Any, Dict

from fastapi.testclient import TestClient
from socketio import AsyncClient

from . import globals
from .nicegui import get_client_id, handle_handshake

RELAY_HOST = 'http://192.168.0.111'


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
        def on_handshake(environ: Dict[str, Any]) -> Dict[str, Any]:
            client = globals.clients[get_client_id(environ)]
            client.environ = environ
            return handle_handshake(client)

    async def connect(self) -> None:
        await self.relay.connect(RELAY_HOST, socketio_path='/on_air/socket.io')
