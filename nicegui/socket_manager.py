from typing import Union

import socketio
from fastapi import FastAPI

# TODO:
# based on: https://github.com/pyropy/fastapi-socketio/blob/b37d58f0dc234b517f9ddf5c4c19ccd690f8fe07/fastapi_socketio/socket_manager.py
# once kwargs is available in `fastapi_socketio` package, the package's implementation can be used
# and this copy can be removed. We need kwargs in order to pass the json parameter to AsyncServer.


class SocketManager:
    """
    Integrates SocketIO with FastAPI app.
    Adds `sio` property to FastAPI object (app).

    Default mount location for SocketIO app is at `/ws`
    and default SocketIO path is `socket.io`.
    (e.g. full path: `ws://www.example.com/ws/socket.io/)

    SocketManager exposes basic underlying SocketIO functionality.

    e.g. emit, on, send, call, etc.
    """

    def __init__(
        self,
        app: FastAPI,
        mount_location: str = "/ws",
        socketio_path: str = "socket.io",
        cors_allowed_origins: Union[str, list] = '*',
        async_mode: str = "asgi",
        **kwargs
    ) -> None:
        # TODO: Change Cors policy based on fastapi cors Middleware
        self._sio = socketio.AsyncServer(async_mode=async_mode, cors_allowed_origins=cors_allowed_origins, **kwargs)
        self._app = socketio.ASGIApp(
            socketio_server=self._sio, socketio_path=socketio_path
        )

        app.mount(mount_location, self._app)
        app.sio = self._sio

    def is_asyncio_based(self) -> bool:
        return True

    @property
    def on(self):
        return self._sio.on

    @property
    def attach(self):
        return self._sio.attach

    @property
    def emit(self):
        return self._sio.emit

    @property
    def send(self):
        return self._sio.send

    @property
    def call(self):
        return self._sio.call

    @property
    def close_room(self):
        return self._sio.close_room

    @property
    def get_session(self):
        return self._sio.get_session

    @property
    def save_session(self):
        return self._sio.save_session

    @property
    def session(self):
        return self._sio.session

    @property
    def disconnect(self):
        return self._sio.disconnect

    @property
    def handle_request(self):
        return self._sio.handle_request

    @property
    def start_background_task(self):
        return self._sio.start_background_task

    @property
    def sleep(self):
        return self._sio.sleep

    @property
    def enter_room(self):
        return self._sio.enter_room

    @property
    def leave_room(self):
        return self._sio.leave_room
