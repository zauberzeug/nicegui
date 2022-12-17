import inspect
import logging
import uuid

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware

EXCLUDED_USER_AGENTS = ('bot', 'spider', 'crawler', 'monitor', 'curl',
                        'wget', 'python-requests', 'kuma', 'health check')


def start_monitor(app: FastAPI):
    try:
        import prometheus_client
        visits = prometheus_client.Counter('nicegui_page_visits', 'Number of real page visits', [
                                           'path', 'session', 'origin'])

        class PrometheusMiddleware(BaseHTTPMiddleware):
            async def dispatch(self, request: Request, call_next):
                if 'id' not in request.session:
                    request.session['id'] = str(uuid.uuid4())
                response = await call_next(request)
                if response.headers.get('x-nicegui-content') == 'page':
                    agent = request.headers.get('user-agent', 'unknown').lower()
                    # ignore monitoring, web crawlers and the like
                    if not any(s in agent for s in EXCLUDED_USER_AGENTS):
                        origin_url = request.headers.get('referer', 'unknown')
                        print(request.get('path'), agent, request.session['id'], origin_url, flush=True)
                        visits.labels(request.get('path'), request.session['id'], origin_url).inc()
                return response

        if inspect.stack()[-2].filename.endswith('spawn.py'):
            prometheus_client.start_http_server(9062)

        app.add_middleware(PrometheusMiddleware)
        app.add_middleware(SessionMiddleware, secret_key='NiceGUI is awesome!')
    except ModuleNotFoundError:
        logging.info('Prometheus not installed, skipping monitoring')
