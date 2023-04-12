import asyncssh
import socketio

from . import background_tasks


class Server(asyncssh.SSHServer):
    def __init__(self, air):
        self.air = air

    def connection_made(self, conn):
        self._conn = conn

    def begin_auth(self, username):
        return False  # Allow anonymous access

    async def session_requested(self):
        return Session(self.air)


class Session(asyncssh.SSHServerSession):
    def __init__(self, relay: socketio.AsyncClient):
        self.relay = relay

    def connection_made(self, chan):
        self._chan = chan

    def shell_requested(self):
        return True

    def exec_requested(self, command):
        return False

    def data_received(self, data, datatype):
        background_tasks.create(self.relay.emit('ssh_data', {'data': data}))

    async def eof_received(self):
        return True
