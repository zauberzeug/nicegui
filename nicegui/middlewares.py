from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class RedirectWithPrefixMiddleware(BaseHTTPMiddleware):
    """
    Middleware that redirects the response Location header with a prefix.

    This middleware is designed to be used in web applications that are deployed behind a reverse proxy or load balancer
    which adds a prefix to the URL. It intercepts the response and modifies the Location header by adding the prefix
    before the original URL.

    Usage:
    1. Create an instance of RedirectWithPrefixMiddleware and add it to your application's middleware stack.
    2. Ensure that your reverse proxy or load balancer sets the 'X-Forwarded-Prefix' header in the incoming request.
    3. When a response with a Location header starting with '/' is received, this middleware will prepend the prefix
       to the Location URL.

    Example:
    ```python
    from nicegui.middlewares import RedirectWithPrefixMiddleware

    app = FastAPI()

    app.add_middleware(RedirectWithPrefixMiddleware)

    @app.get("/")
    async def root():
        return {"message": "Hello, World!"}
    ```

    Attributes:
    - BaseHTTPMiddleware: The base class for HTTP middleware in the application.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Dispatch method called for each incoming request.

        Args:
        - request (Request): The incoming request object.
        - call_next (RequestResponseEndpoint): The next middleware or endpoint to call.

        Returns:
        - Response: The response object.

        Raises:
        - None.

        This method intercepts the response and modifies the Location header by adding the prefix before the original URL.
        """
        prefix = request.headers.get('X-Forwarded-Prefix', '')
        response = await call_next(request)
        if 'Location' in response.headers and response.headers['Location'].startswith('/'):
            new_location = prefix + response.headers['Location']
            response.headers['Location'] = new_location
        return response
