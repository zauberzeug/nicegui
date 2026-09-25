import socketio

from nicegui import Client, app, ui
from nicegui.air import _handle_handshake
from nicegui.testing import User


def test_engineio_state_contract() -> None:
    assert socketio.AsyncClient().eio.state == 'disconnected', \
        'Air.connect() detects a stale Socket.IO connection via this Engine.IO state'


async def test_air_handshake_creates_tab_storage(user: User) -> None:
    @ui.page('/')
    def index():
        pass

    template = await user.open('/')
    client = Client(template.page, request=template.request)

    assert await _handle_handshake({
        'client_id': client.id,
        'sid': 'air-sid',
        'tab_id': 'air-tab',
        'environ': {'QUERY_STRING': f'client_id={client.id}'},
        'document_id': 'air-doc',
    })

    with client:
        app.storage.tab['x'] = 1
        assert app.storage.tab['x'] == 1
