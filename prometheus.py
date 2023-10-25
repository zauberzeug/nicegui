import inspect
import logging
import uuid

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

EXCLUDED_USER_AGENTS = {'bot', 'spider', 'crawler', 'monitor', 'curl',
                        'wget', 'python-requests', 'kuma', 'health check'}


def start_monitor(app: FastAPI) -> None:
    try:
        import prometheus_client
    except ModuleNotFoundError:
        logging.info('Prometheus not installed, skipping monitoring')
        return

    visits = prometheus_client.Counter('nicegui_page_visits', 'Number of real page visits',
                                       ['path', 'session', 'origin'])

    class PrometheusMiddleware(BaseHTTPMiddleware):

        async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
            if 'id' not in request.session:
                request.session['id'] = str(uuid.uuid4())
            response = await call_next(request)
            if response.headers.get('x-nicegui-content') == 'page':
                agent = request.headers.get('user-agent', 'unknown').lower()
                # ignore monitoring, web crawlers and the like
                if not any(s in agent for s in EXCLUDED_USER_AGENTS):
                    origin_url = request.headers.get('referer', 'unknown')
                    visits.labels(request.get('path'), request.session['id'], origin_url).inc()
            return response

    if inspect.stack()[-2].filename.endswith('spawn.py'):
        prometheus_client.start_http_server(9062)

    app.add_middleware(PrometheusMiddleware)
