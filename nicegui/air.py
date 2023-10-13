import asyncio
import gzip
import re
from typing import Any, Dict

import httpx
import socketio
from socketio import AsyncClient

from . import background_tasks, globals  # pylint: disable=redefined-builtin
from .nicegui import handle_disconnect, handle_event, handle_handshake, handle_javascript_response

RELAY_HOST = 'https://on-air.nicegui.io/'


class Air:

    def __init__(self, token: str) -> None:
        self.token = token
        self.relay = AsyncClient()
        self.client = httpx.AsyncClient(app=globals.app)
        self.connecting = False

        @self.relay.on('http')
        async def on_http(data: Dict[str, Any]) -> Dict[str, Any]:
            headers: Dict[str, Any] = data['headers']
            headers.update({'Accept-Encoding': 'identity', 'X-Forwarded-Prefix': data['prefix']})
            url = 'http://test' + data['path']
            request = self.client.build_request(
                data['method'],
                url,
                params=data['params'],
                headers=headers,
                content=data['body'],
            )
            response = await self.client.send(request)
            instance_id = data['instance-id']
            content = response.content.replace(
                b'const extraHeaders = {};',
                (f'const extraHeaders = {{ "fly-force-instance-id" : "{instance_id}" }};').encode(),
            )
            match = re.search(b'const query = ({.*?})', content)
            if match:
                new_js_object = match.group(1).decode().rstrip('}') + ", 'fly_instance_id' : '" + instance_id + "'}"
                content = content.replace(match.group(0), f'const query = {new_js_object}'.encode())
            compressed = gzip.compress(content)
            response.headers.update({'content-encoding': 'gzip', 'content-length': str(len(compressed))})
            return {
                'status_code': response.status_code,
                'headers': response.headers.multi_items(),
                'content': compressed,
            }

        @self.relay.on('ready')
        def on_ready(data: Dict[str, Any]) -> None:
            globals.app.urls.add(data['device_url'])
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
            client.disconnect_task = background_tasks.create(handle_disconnect(client))

        @self.relay.on('event')
        def on_event(data: Dict[str, Any]) -> None:
            client_id = data['client_id']
            if client_id not in globals.clients:
                return
            client = globals.clients[client_id]
            if isinstance(data['msg']['args'], dict) and 'socket_id' in data['msg']['args']:
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
            print('Sorry, you have reached the time limit of this NiceGUI On Air preview.', flush=True)
            await self.connect()

        @self.relay.on('reconnect')
        async def on_reconnect(_: Dict[str, Any]) -> None:
            await self.connect()

    async def connect(self) -> None:
        if self.connecting:
            return
        self.connecting = True
        backoff_time = 1
        while True:
            try:
                if self.relay.connected:
                    await self.relay.disconnect()
                await self.relay.connect(
                    f'{RELAY_HOST}?device_token={self.token}',
                    socketio_path='/on_air/socket.io',
                    transports=['websocket', 'polling'],  # favor websocket over polling
                )
                break
            except socketio.exceptions.ConnectionError:
                pass
            except ValueError:  # NOTE this sometimes happens when the internal socketio client is not yet ready
                await self.relay.disconnect()
            except Exception:
                globals.log.exception('Could not connect to NiceGUI On Air server.')

            await asyncio.sleep(backoff_time)
            backoff_time = min(backoff_time * 2, 32)
        self.connecting = False

    async def disconnect(self) -> None:
        await self.relay.disconnect()

    async def emit(self, message_type: str, data: Dict[str, Any], room: str) -> None:
        if self.relay.connected:
            await self.relay.emit('forward', {'event': message_type, 'data': data, 'room': room})
