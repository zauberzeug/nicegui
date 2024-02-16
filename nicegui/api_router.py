from pathlib import Path
from typing import Callable, Optional, Union

import fastapi

from .page import page as ui_page


class APIRouter(fastapi.APIRouter):
    """
    Extends the `fastapi.APIRouter` class to provide additional functionality for creating pages in NiceGUI.

    Usage:
    ------
    router = APIRouter()

    @router.page(path='/my-page', title='My Page', viewport='width=device-width, initial-scale=1.0')
    def my_page():
        # Page logic goes here
        pass

    Parameters:
    -----------
    path : str
        The route of the new page (path must start with '/').
    title : Optional[str], default None
        Optional page title.
    viewport : Optional[str], default None
        Optional viewport meta tag content.
    favicon : Optional[Union[str, Path]], default None
        Optional relative filepath or absolute URL to a favicon. If not provided, the NiceGUI icon will be used.
    dark : Optional[bool], default None
        Whether to use Quasar's dark mode. If not provided, it defaults to the `dark` argument of the `run` command.
    response_timeout : float, default 3.0
        Maximum time for the decorated function to build the page.
    **kwargs : dict
        Additional keyword arguments passed to FastAPI's `@app.get` method.

    Returns:
    --------
    Callable
        A decorator function that can be used to create a new page at the given route.

    Notes:
    ------
    - Each user will see a new instance of the page. This means it is private to the user and not shared with others.
    - The decorated function should contain the logic for building the page.

    Example:
    --------
    router = APIRouter()

    @router.page(path='/my-page', title='My Page', viewport='width=device-width, initial-scale=1.0')
    def my_page():
        # Page logic goes here
        pass
    """
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
        (as it is done [when placing elements outside of a page decorator ](https://nicegui.io/documentation/section_pages_routing#auto-index_page)).

        Parameters:
        -----------
        path : str
            The route of the new page (path must start with '/').
        title : Optional[str], default None
            Optional page title.
        viewport : Optional[str], default None
            Optional viewport meta tag content.
        favicon : Optional[Union[str, Path]], default None
            Optional relative filepath or absolute URL to a favicon. If not provided, the NiceGUI icon will be used.
        dark : Optional[bool], default None
            Whether to use Quasar's dark mode. If not provided, it defaults to the `dark` argument of the `run` command.
        response_timeout : float, default 3.0
            Maximum time for the decorated function to build the page.
        **kwargs : dict
            Additional keyword arguments passed to FastAPI's `@app.get` method.

        Returns:
        --------
        Callable
            A decorator function that can be used to create a new page at the given route.
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
