from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from . import core
from .version import __version__

import re
from starlette.middleware import Middleware
from starlette.types import ASGIApp, Receive, Scope, Send

class RedirectWithPrefixMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        prefix = request.headers.get('X-Forwarded-Prefix', '')
        response = await call_next(request)
        if 'Location' in response.headers and response.headers['Location'].startswith('/'):
            new_location = prefix + response.headers['Location']
            response.headers['Location'] = new_location
        return response


class SetCacheControlMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if request.url.path.startswith(f'/_nicegui/{__version__}/') \
                and not request.url.path.startswith(f'/_nicegui/{__version__}/dynamic_resources/'):
            response.headers['Cache-Control'] = core.app.config.cache_control_directives
        return response

class RedirectWithPrefixMiddlewareSubApp(Middleware):
    def __init__(self, app: ASGIApp, root_path: str = '', mount_path: str = '/'):
        super().__init__(app)
        self._app=app
        self._path_prefix = root_path.rstrip('/')
        self._mount_path = mount_path.rstrip('/') or '/'
        # Patterns for static files that shouldn't get path modification
        self._static_patterns = [
            re.compile(r'^/_nicegui/'),
            re.compile(r'^/_static/'),
            re.compile(r'^/_favicon\.ico$'),
            re.compile(r'^/_favicon\.png$')
        ]
        # Pattern for file extensions
        self._file_extension_pattern = re.compile(r'\.[a-z]{2,5}$')

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope['type'] == 'websocket':
            # Handle WebSocket connections
            if scope['path'].startswith(self._mount_path):
                new_path = f"{self._path_prefix}{scope['path']}"
                if not new_path.endswith('/'):
                    new_path += '/'
                scope['path'] = new_path

        elif scope['type'] == 'http':
            if scope['path'].startswith(self._mount_path):
                old_path = scope['path']
                new_path = f"{self._path_prefix}{old_path}"
                if not new_path.endswith('/') and not self._file_extension_pattern.search(new_path.rstrip('/')):
                    new_path += '/'
                scope['path'] = new_path
