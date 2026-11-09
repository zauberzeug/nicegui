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
        target = _documentation_redirect(request.url.path)
        is_www = request.url.hostname == 'www.nicegui.io'
        if target is None and not is_www:
            return await call_next(request)
        path, _, fragment = (target or request.url.path).partition('#')
        location = (sitemap.SITE_URL if is_www else '') + path
        if request.url.query:
            location += f'?{request.url.query}'
        if fragment:
            location += f'#{fragment}'
        return RedirectResponse(location, status_code=301)


def _documentation_redirect(path: str) -> str | None:
    """Return the new path of a renamed documentation page (with an optional anchor), or ``None``."""
    slug = next((slug for slug in i18n.LANGUAGES if slug != 'en' and path.startswith(f'/{slug}/')), 'en')
    prefix = i18n.url('/documentation/', language=slug)
    if not path.startswith(prefix):
        return None
    target = documentation.redirects.get(path.removeprefix(prefix).rstrip('/'))
    return i18n.url(f'/documentation/{target}', language=slug) if target else None
