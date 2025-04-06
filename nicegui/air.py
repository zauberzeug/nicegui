from __future__ import annotations

import asyncio
import gzip
import json
import logging
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, AsyncIterator, Dict, Optional
from uuid import uuid4

import socketio
import socketio.exceptions

from . import background_tasks, core
from .client import Client
from .dataclasses import KWONLY_SLOTS
from .elements.timer import Timer as timer
from .logging import log

if TYPE_CHECKING:
    import httpx

RELAY_HOST = 'https://on-air.nicegui.io/'


@dataclass(**KWONLY_SLOTS)
class Stream:
    data: AsyncIterator[bytes]
    response: Optional[httpx.Response] = None


class Air:
    # Chunk size constants
    HTTP_CHUNK_SIZE = 512 * 1024  # 512 KB for efficient bulk transfer
    STREAM_CHUNK_SIZE = 64 * 1024  # 64 KB for smooth streaming

    def __init__(self, token: str) -> None:
        import httpx  # pylint: disable=import-outside-toplevel

        self.log = logging.getLogger('nicegui.air')
        self.token = token
        self.relay = socketio.AsyncClient()
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=core.app))
        self.streaming_client = httpx.AsyncClient()
        self.connecting = False
        self.streams: Dict[str, Stream] = {}
        self.remote_url: Optional[str] = None

        timer(5, self.connect)  # ensure we stay connected

        @self.relay.on('http')
        async def _handle_http(data: Dict[str, Any]) -> Dict[str, Any]:
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
            self.client.cookies.clear()
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
            total_size = len(compressed)
            response.headers.update({'content-encoding': 'gzip', 'content-length': str(total_size)})
            result = {
                'status_code': response.status_code,
                'headers': response.headers.multi_items(),
                'content': compressed,
            }

            if total_size > self.HTTP_CHUNK_SIZE:
                stream_id = self._create_chunked_stream(compressed, self.HTTP_CHUNK_SIZE, response)
                result['stream_id'] = stream_id
                result['total_size'] = total_size
                del result['content']

            return result

        @self.relay.on('range-request')
        async def _handle_range_request(data: Dict[str, Any]) -> Dict[str, Any]:
            headers: Dict[str, Any] = data['headers']
            url = next(iter(u for u in core.app.urls if self.remote_url != u)) + data['path']
            data['params']['nicegui_chunk_size'] = self.STREAM_CHUNK_SIZE
            request = self.client.build_request(
                data['method'],
                url,
                params=data['params'],
                headers=headers,
            )
            response = await self.streaming_client.send(request, stream=True)
            stream_id = str(uuid4())
            self.streams[stream_id] = Stream(data=response.aiter_bytes(), response=response)
            return {
                'status_code': response.status_code,
                'headers': response.headers.multi_items(),
                'stream_id': stream_id,
            }

        @self.relay.on('read-stream')
        async def _handle_read_stream(stream_id: str) -> Optional[bytes]:
            try:
                return await self.streams[stream_id].data.__anext__()
            except StopAsyncIteration:
                await _handle_close_stream(stream_id)
                return None
            except Exception:
                await _handle_close_stream(stream_id)
                raise

        @self.relay.on('close-stream')
        async def _handle_close_stream(stream_id: str) -> None:
            response = self.streams[stream_id].response
            if response:
                await response.aclose()
            del self.streams[stream_id]

        @self.relay.on('ready')
        def _handle_ready(data: Dict[str, Any]) -> None:
            core.app.urls.add(data['device_url'])
            self.remote_url = data['device_url']
            if core.app.config.show_welcome_message:
                print(f'NiceGUI is on air at {data["device_url"]}', flush=True)

        @self.relay.on('error')
        def _handleerror(data: Dict[str, Any]) -> None:
            print('Error:', data['message'], flush=True)

        @self.relay.on('handshake')
        def _handle_handshake(data: Dict[str, Any]) -> bool:
            client_id = data['client_id']
            if client_id not in Client.instances:
                return False
            client = Client.instances[client_id]
            client.environ = data['environ']
            if data.get('old_tab_id'):
                core.app.storage.copy_tab(data['old_tab_id'], data['tab_id'])
            client.tab_id = data['tab_id']
            client.on_air = True
            client.handle_handshake(data['sid'], data['document_id'], data.get('next_message_id'))
            return True

        @self.relay.on('client_disconnect')
        def _handle_client_disconnect(data: Dict[str, Any]) -> None:
            self.log.debug('client disconnected.')
            client_id = data['client_id']
            if client_id not in Client.instances:
                return
            Client.instances[client_id].handle_disconnect(data['sid'])

        @self.relay.on('connect')
        async def _handle_connect() -> None:
            self.log.debug('connected.')

        @self.relay.on('disconnect')
        async def _handle_disconnect() -> None:
            self.log.debug('disconnected.')

        @self.relay.on('connect_error')
        async def _handle_connect_error(data) -> None:
            message = data.get('message', 'Unknown error') if isinstance(data, dict) else data
            self.log.warning(f'Connection error: {message}')

        @self.relay.on('event')
        def _handle_event(data: Dict[str, Any]) -> None:
            client_id = data['client_id']
            if client_id not in Client.instances:
                return
            client = Client.instances[client_id]
            args = data['msg']['args']
            if args and isinstance(args[0], str) and args[0].startswith('{"socket_id":'):
                arg0 = json.loads(args[0])
                arg0['socket_id'] = client_id  # HACK: translate socket_id of ui.scene's init event
                args[0] = json.dumps(arg0)
            client.handle_event(data['msg'])

        @self.relay.on('javascript_response')
        def _handle_javascript_response(data: Dict[str, Any]) -> None:
            client_id = data['client_id']
            if client_id not in Client.instances:
                return
            client = Client.instances[client_id]
            client.handle_javascript_response(data['msg'])

        @self.relay.on('ack')
        def _handle_ack(data: Dict[str, Any]) -> None:
            client_id = data['client_id']
            if client_id not in Client.instances:
                return
            client = Client.instances[client_id]
            client.outbox.prune_history(data['msg']['next_message_id'])

        @self.relay.on('out_of_time')
        async def _handle_out_of_time() -> None:
            print('Sorry, you have reached the time limit of this NiceGUI On Air preview.', flush=True)
            await self.connect()

    def _create_chunked_stream(self, data: bytes, chunk_size: int, response: Optional[httpx.Response] = None) -> str:
        """Create a chunked stream for large data."""
        async def chunk_iterator() -> AsyncIterator[bytes]:
            for i in range(0, len(data), chunk_size):
                yield data[i:i + chunk_size]

        stream_id = str(uuid4())
        self.streams[stream_id] = Stream(data=chunk_iterator(), response=response)
        return stream_id

    async def connect(self) -> None:
        """Connect to the NiceGUI On Air server."""
        if self.connecting:
            self.log.debug('Already connecting.')
            return
        if self.relay.connected:
            return
        self.log.debug('Going to connect...')
        self.connecting = True
        try:
            if self.relay.connected:
                await asyncio.wait_for(self.disconnect(), timeout=5)
            self.log.debug('Connecting...')
            await self.relay.connect(
                f'{RELAY_HOST}?device_token={self.token}',
                socketio_path='/on_air/socket.io',
                transports=['websocket', 'polling'],  # favor websocket over polling
                wait_timeout=5,
            )
            assert self.relay.connected
            return
        except socketio.exceptions.ConnectionError:
            self.log.debug('Connection error.', stack_info=True)
        except ValueError:  # NOTE this sometimes happens when the internal socketio client is not yet ready
            self.log.debug('ValueError while connecting.', stack_info=True)
        except Exception:
            log.exception('Could not connect to NiceGUI On Air server.')
        finally:
            self.connecting = False

    async def disconnect(self) -> None:
        """Disconnect from the NiceGUI On Air server."""
        self.log.debug('Disconnecting...')
        if self.relay.connected:
            await self.relay.disconnect()
        for stream in self.streams.values():
            if stream.response:
                await stream.response.aclose()
        self.streams.clear()
        self.log.debug('Disconnected.')

    async def emit(self, message_type: str, data: Dict[str, Any], room: str) -> None:
        """Emit a message to the NiceGUI On Air server."""
        if not self.relay.connected:
            return
        if isinstance(data, dict) and 'src' in data and isinstance(data['src'], bytes):
            src = data['src']
            total_size = len(src)
            if total_size > self.HTTP_CHUNK_SIZE:
                stream_id = self._create_chunked_stream(src, self.HTTP_CHUNK_SIZE)
                del data['src']
                data['src_stream_id'] = stream_id
        await self.relay.emit('forward', {'event': message_type, 'data': data, 'room': room})

    @staticmethod
    def is_air_target(target_id: str) -> bool:
        """Whether the given target ID is an On Air client or a SocketIO room."""
        if target_id in Client.instances:
            return Client.instances[target_id].on_air
        return target_id in core.sio.manager.rooms


def connect() -> None:
    """Connect to the NiceGUI On Air server if there is an air instance."""
    if core.air:
        background_tasks.create(core.air.connect())


def disconnect() -> None:
    """Disconnect from the NiceGUI On Air server if there is an air instance."""
    if core.air:
        background_tasks.create(core.air.disconnect())
