from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from nicegui import app, core

from . import documentation, i18n, sitemap


def setup() -> None:
    """Add the website's middlewares for cache control and permanent redirects."""
    app.add_middleware(DocsSetCacheControlMiddleware)
    app.add_middleware(PermanentRedirectMiddleware)


class DocsSetCacheControlMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if request.url.path.startswith('/fonts/') or request.url.path.startswith('/static/'):
            response.headers['Cache-Control'] = core.app.config.cache_control_directives
        elif request.url.path.startswith('/examples/images/'):
            response.headers['Cache-Control'] = 'public, max-age=86400'  # 1 day
        return response


class PermanentRedirectMiddleware(BaseHTTPMiddleware):
    """Redirect www.nicegui.io and renamed documentation pages so that search engines see a single URL per page."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path
        prefix = next((f'/{slug}' for slug in i18n.LANGUAGES if slug != 'en' and path.startswith(f'/{slug}/')), '')
        name = path.removeprefix(f'{prefix}/documentation/')
        if name != path and name in documentation.redirects:
            path, _, fragment = f'{prefix}/documentation/{documentation.redirects[name]}'.partition('#')
        else:
            fragment = ''
        is_www = request.url.hostname == 'www.nicegui.io'
        if path == request.url.path and not is_www:
            return await call_next(request)
        location = (sitemap.SITE_URL if is_www else '') + path
        if request.url.query:
            location += f'?{request.url.query}'
        if fragment:
            location += f'#{fragment}'
        return RedirectResponse(location, status_code=301)
