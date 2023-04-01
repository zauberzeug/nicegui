from socketio import AsyncClient

RELAY_HOST = 'http://192.168.0.111'


class Air:

    def __init__(self) -> None:
        self.relay = AsyncClient()

    async def connect(self) -> None:
        await self.relay.connect(RELAY_HOST, socketio_path='/on_air/socket.io', headers={'NiceGUI': 'register_relay'})
