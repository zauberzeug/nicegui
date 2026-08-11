import socketio


def test_engineio_state_contract() -> None:
    assert socketio.AsyncClient().eio.state == 'disconnected', \
        'Air.connect() detects a stale Socket.IO connection via this Engine.IO state'
