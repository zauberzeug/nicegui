from pathlib import Path
from typing import Callable, Optional, Union

import fastapi

from .page import page as ui_page


class APIRouter(fastapi.APIRouter):

    def page(self,
             path: str, *,
             title: Optional[str] = None,
             viewport: Optional[str] = None,
             favicon: Optional[Union[str, Path]] = None,
             dark: Optional[bool] = ...,  # type: ignore
             response_timeout: float = 3.0,
             **kwargs,
             ) -> Callable:
        """Page

        Creates a new page at the given route.
        Each user will see a new instance of the page.
        This means it is private to the user and not shared with others
        (as it is done `when placing elements outside of a page decorator <https://nicegui.io/documentation/section_pages_routing#auto-index_page>`_).

        :param path: route of the new page (path must start with '/')
        :param title: optional page title
        :param viewport: optional viewport meta tag content
        :param favicon: optional relative filepath or absolute URL to a favicon (default: `None`, NiceGUI icon will be used)
        :param dark: whether to use Quasar's dark mode (defaults to `dark` argument of `run` command)
        :param response_timeout: maximum time for the decorated function to build the page (default: 3.0)
        :param kwargs: additional keyword arguments passed to FastAPI's @app.get method
        """
        return ui_page(
            path,
            title=title,
            viewport=viewport,
            favicon=favicon,
            dark=dark,
            response_timeout=response_timeout,
            api_router=self,
            **kwargs
        )
