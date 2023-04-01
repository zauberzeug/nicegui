from typing import Any, Dict

from fastapi.testclient import TestClient
from socketio import AsyncClient

from . import globals

RELAY_HOST = 'http://192.168.0.111'


class Air:

    def __init__(self) -> None:
        self.relay = AsyncClient()
        self.test_client = TestClient(globals.app)

        @self.relay.on('get')
        def on_get(data: Dict[str, Any]) -> Dict[str, Any]:
            print(f'get {data["path"]}', flush=True)
            response = self.test_client.get(data['path'])
            return {
                'status_code': response.status_code,
                'content': response.content,
                'media_type': response.headers.get('content-type'),
            }

    async def connect(self) -> None:
        await self.relay.connect(RELAY_HOST, socketio_path='/on_air/socket.io', headers={'NiceGUI': 'register_relay'})
