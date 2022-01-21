import json

from starlette import websockets
from websockets import exceptions


async def send_json_monkey_patched(self, data, mode: str = "text") -> None:
    """
    Copy of the websockets.WebSocket.send_json extended with a try/except to monkeypatch the original.
    """
    assert mode in ["text", "binary"]
    text = json.dumps(data)
    if mode == "text":
        try:
            await self.send({"type": "websocket.send", "text": text})
        except (exceptions.ConnectionClosedError, RuntimeError,exceptions.ConnectionClosedOK):
            pass
    else:
        await self.send({"type": "websocket.send", "bytes": text.encode("utf-8")})


def monkeypatch():
    websockets.WebSocket.send_json = send_json_monkey_patched
