from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from . import globals, ui


class RequestTrackingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        ui.session.set(request.session)
        response = await call_next(request)
        return response
