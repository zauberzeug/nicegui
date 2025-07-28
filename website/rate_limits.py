from nicegui import app

try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.errors import RateLimitExceeded
    from slowapi.middleware import SlowAPIMiddleware
    from slowapi.util import get_remote_address

    HAS_SLOWAPI = True
except ImportError:
    HAS_SLOWAPI = False


def setup() -> None:
    if not HAS_SLOWAPI:
        return
    limiter = Limiter(key_func=get_remote_address, default_limits=['50/minute', '5/second'])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)
