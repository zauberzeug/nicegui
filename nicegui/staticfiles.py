from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.types import Scope


class CacheControlledStaticFiles(StaticFiles):

    async def get_response(self, path: str, scope: Scope) -> Response:
        response = await super().get_response(path, scope)
        response.headers['Cache-Control'] = 'public, max-age=3600'
        return response
