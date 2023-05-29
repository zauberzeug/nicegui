import contextvars
from typing import Any, Dict

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

request_contextvar = contextvars.ContextVar('request_var')


class RequestTrackingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_contextvar.set(request)
        return await call_next(request)


class Storage:

    @property
    def session(self) -> Dict:
        return request_contextvar.get().session
