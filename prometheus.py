import inspect
import logging
import uuid

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

EXCLUDED_USER_AGENTS = {'bot', 'spider', 'crawler', 'monitor', 'curl',
                        'wget', 'python-requests', 'kuma', 'health check'}


def start_monitor(app: FastAPI) -> None:
    """
    Starts the Prometheus monitoring for the NiceGUI application.

    This function enables monitoring of page visits using Prometheus. It checks if the Prometheus client library is
    installed and if not, it logs a message and returns. If the library is installed, it creates a Counter metric
    named 'nicegui_page_visits' to track the number of real page visits. The metric has three labels: 'path', 'session',
    and 'origin'.

    The function also defines a PrometheusMiddleware class that extends the BaseHTTPMiddleware class. This middleware
    is responsible for incrementing the 'nicegui_page_visits' metric for each real page visit. It checks if the
    'id' key is present in the session, and if not, it generates a new UUID and assigns it to the 'id' key. Then, it
    checks if the response has the 'x-nicegui-content' header set to 'page'. If it does, it extracts the user agent
    from the request headers and checks if it matches any of the excluded user agents defined in the
    EXCLUDED_USER_AGENTS list. If the user agent is not excluded, it retrieves the origin URL from the 'referer'
    header and increments the 'nicegui_page_visits' metric with the corresponding labels.

    If the code is being executed from the 'spawn.py' file, it starts an HTTP server on port 9062 using the
    prometheus_client library.

    Finally, the PrometheusMiddleware is added as a middleware to the FastAPI application.

    - app: The FastAPI application object.
    :type app: FastAPI
    """
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
