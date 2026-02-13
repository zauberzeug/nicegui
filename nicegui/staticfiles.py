try:
    from starlette.responses import Response
    from starlette.staticfiles import StaticFiles
    from starlette.types import Scope
    _StaticFilesBase = StaticFiles
except ImportError:
    Response = None  # type: ignore
    StaticFiles = None  # type: ignore
    Scope = None  # type: ignore
    _StaticFilesBase = object  # type: ignore


class CacheControlledStaticFiles(_StaticFilesBase):

    def __init__(self, *args, max_cache_age: int = 3600, **kwargs) -> None:
        self.max_cache_age = max_cache_age
        super().__init__(*args, **kwargs)

    async def get_response(self, path: str, scope: Scope) -> Response:
        response = await super().get_response(path, scope)
        response.headers['Cache-Control'] = f'public, max-age={self.max_cache_age}'
        return response
