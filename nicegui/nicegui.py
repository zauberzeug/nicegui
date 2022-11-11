import asyncio
import urllib.parse
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_socketio import SocketManager

from . import globals, vue
from .client import Client

globals.app = app = FastAPI(routes=vue.generate_js_routes())
globals.sio = sio = SocketManager(app=app)._sio

app.add_middleware(GZipMiddleware)

Client().__enter__()


@app.get('/')
def index():
    return globals.client_stack[-1].build_response()


@app.on_event('startup')
def on_startup() -> None:
    globals.loop = asyncio.get_running_loop()


@sio.on('connect')
async def handle_connect(sid: str, _) -> None:
    client = get_client(sid)
    client.environ = sio.get_environ(sid)
    sio.enter_room(sid, str(client.id))


@sio.on('event')
def handle_event(sid: str, msg: Dict) -> None:
    client = get_client(sid)
    with client:
        sender = client.elements.get(msg['id'])
        if sender:
            sender.handle_event(msg)


def get_client(sid: str) -> Client:
    query_bytes: bytearray = sio.get_environ(sid)['asgi.scope']['query_string']
    query = urllib.parse.parse_qs(query_bytes.decode())
    client_id = int(query['client_id'][0])
    return globals.clients[client_id]
