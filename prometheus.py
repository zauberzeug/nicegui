import inspect
import logging
import uuid
import re

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

EXCLUDED_USER_AGENTS = {'bot', 'spider', 'crawler', 'monitor', 'curl',
                        'wget', 'python-requests', 'kuma', 'health check'}
EXCLUDED_AGENT_PATTERN = re.compile("|".join(EXCLUDED_USER_AGENTS), re.IGNORECASE)

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
            try:
                session_id = get_or_set_session_id(request)
                response = await call_next(request)

                if response.headers.get('x-nicegui-content') == 'page':
                    agent = request.headers.get('user-agent', 'unknown').lower()
                    # ignore monitoring, web crawlers, and bots
                    if not EXCLUDED_AGENT_PATTERN.search(agent):
                        origin_url = request.headers.get('referer', 'unknown')
                        visits.labels(request.url.path, session_id, origin_url).inc()
                return response
            except Exception as e:
                logging.error(f"Error in PrometheusMiddleware: {str(e)}")
                return await call_next(request)

    def get_or_set_session_id(request: Request) -> str:
        if 'id' not in request.session:
            session_id = str(uuid.uuid4())
            request.session['id'] = session_id
        else:
            session_id = request.session['id']
        return session_id

    # Only start Prometheus server in specific conditions (e.g., specific processes)
    if inspect.stack()[-2].filename.endswith('spawn.py'):
        prometheus_client.start_http_server(9062)

    app.add_middleware(PrometheusMiddleware)
