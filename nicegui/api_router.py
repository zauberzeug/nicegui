from typing import Callable

import fastapi

from .page import page as ui_page


class APIRouter(fastapi.APIRouter):

    def page(self, *args, **kwargs) -> Callable:
        return ui_page(*args, api_router=self, **kwargs)
