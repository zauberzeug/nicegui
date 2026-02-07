import secrets

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from . import core
from .version import __version__


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


class CSPMiddleware(BaseHTTPMiddleware):
    """Middleware that generates per-request nonces and adds Content-Security-Policy headers."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Generate a cryptographically secure nonce for this request
        nonce = secrets.token_urlsafe(16)
        request.state.csp_nonce = nonce

        response = await call_next(request)

        # Only add CSP header to HTML responses (pages, not API endpoints or static files)
        if core.app.config.csp_enabled and response.headers.get('X-NiceGUI-Content') == 'page':
            csp_directives = [
                f"script-src 'nonce-{nonce}' 'strict-dynamic'",
                f"style-src 'self' 'nonce-{nonce}' 'unsafe-inline'",  # self for external CSS, unsafe-inline for Tailwind JIT
                f"style-src-elem 'self' 'nonce-{nonce}' 'unsafe-inline'",  # Explicit policy for <style> and <link> tags
                "font-src 'self' data:",  # Allow fonts from same origin and data URIs
                "img-src 'self' data: https:",  # Allow images from same origin, data URIs, and HTTPS
                "object-src 'none'",
                "base-uri 'none'",
            ]

            # Allow custom CSP directives from config
            if core.app.config.csp_extra_directives:
                csp_directives.extend(core.app.config.csp_extra_directives)

            response.headers['Content-Security-Policy'] = '; '.join(csp_directives)

        return response
