from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Match, Route

from . import core
from .version import __version__


class SlashAgnosticMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        scope = request.scope
        path = scope.get('path', '/')
        if scope.get('type') == 'http' and path != '/':
            def has_route_for(p: str) -> bool:
                scope_ = {'type': 'http', 'path': p, 'method': request.method, 'root_path': scope.get('root_path', '')}
                for r in routes:
                    match, _ = r.matches(scope_)
                    if match is Match.FULL:  # NOTE: Route matches are always FULL or NONE
                        return True
                return False

            routes = [r for r in request.app.routes if isinstance(r, Route)]
            alternative = path[:-1] if path.endswith('/') else path + '/'
            if not has_route_for(path) and has_route_for(alternative):
                scope['path'] = alternative
        return await call_next(request)


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
