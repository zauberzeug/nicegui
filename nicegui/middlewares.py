from starlette.middleware.base import BaseHTTPMiddleware


class RedirectWithPrefixMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        prefix = request.headers.get('X-Forwarded-Prefix', '')
        response = await call_next(request)
        if 'Location' in response.headers:
            new_location = prefix + response.headers['Location']
            response.headers['Location'] = new_location
        return response
