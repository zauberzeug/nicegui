import contextvars
from typing import Dict

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

request_contextvar = contextvars.ContextVar('request_var', default=None)


class ReadOnlyDict:
    def __init__(self, data: Dict, write_error_message: str = 'Read-only dict'):
        self._data = data
        self._write_error_message = write_error_message

    def __getitem__(self, item):
        return self._data[item]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __setitem__(self, key, value):
        raise TypeError(self._write_error_message)


class RequestTrackingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request_contextvar.set(request)
        request.state.responded = False
        response = await call_next(request)
        request.state.responded = True
        request_contextvar.reset(token)
        return response


class Storage:

    @property
    def session(self) -> Dict:
        request: Request = request_contextvar.get()
        if request.state.responded:
            return ReadOnlyDict(
                request.session,
                'the response to the browser has already been build so modifications can not be send back anymore'
            )
        return request.session
