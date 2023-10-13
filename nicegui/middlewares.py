from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class RedirectWithPrefixMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        prefix = request.headers.get('X-Forwarded-Prefix', '')
        response = await call_next(request)
        if 'Location' in response.headers and response.headers['Location'].startswith('/'):
            new_location = prefix + response.headers['Location']
            response.headers['Location'] = new_location
        return response
