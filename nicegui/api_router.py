from typing import Callable

import fastapi

from .page import page as ui_page


class APIRouter(fastapi.APIRouter):

    def page(self, func: Callable) -> Callable:
        return ui_page(func, api_router=self)
