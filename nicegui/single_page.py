from typing import Callable, Dict, Union

from fastapi.routing import APIRoute

from nicegui import background_tasks, helpers, ui, core, Client, app


class RouterFrame(ui.element, component='single_page.js'):
    """The RouterFrame is a special element which is used by the SinglePageRouter to exchange the content of the
    current page with the content of the new page. It serves as container and overrides the browser's history
    management to prevent the browser from reloading the whole page."""

    def __init__(self, base_path: str):
        """
        :param base_path: The base path of the single page router which shall be tracked (e.g. when clicking on links)
        """
        super().__init__()
        self._props["base_path"] = base_path


class SinglePageRouter:
    """The SinglePageRouter allows the development of a Single Page Application (SPA) which maintains a
    persistent connection to the server and only updates the content of the page instead of reloading the whole page.

    This enables the development of complex web applications with large amounts of per-user (per browser tab) data
    which is kept alive for the duration of the connection."""

    def __init__(self, path: str, **kwargs) -> None:
        """
        :param path: the base path of the single page router.
        """
        super().__init__()

        self.routes: Dict[str, Callable] = {}
        self.base_path = path
        self._find_api_routes()

        @ui.page(path, **kwargs)
        @ui.page(f'{path}' + '{_:path}', **kwargs)  # all other pages
        async def root_page(client: Client):
            if app.storage.session.get('__pageContent', None) is None:
                content: Union[ui.element, None] = RouterFrame(self.base_path).on('open', lambda e: self.open(e.args))
                app.storage.session['__pageContent'] = content

    def _find_api_routes(self):
        """Find all API routes already defined via the @page decorator, remove them and redirect them to the
        single page router"""
        page_routes = set()
        for key, route in Client.page_routes.items():
            if (route.startswith(self.base_path) and
                    not route[len(self.base_path):].startswith("_")):
                page_routes.add(route)
                Client.single_page_routes[route] = self
                self.routes[route] = key

        for route in core.app.routes.copy():
            if isinstance(route, APIRoute):
                if route.path in page_routes:
                    core.app.routes.remove(route)

    def add(self, path: str, builder: Callable) -> None:
        """Add a new route to the single page router

        :param path: the path of the route
        :param builder: the builder function"""
        self.routes[path] = builder

    def open(self, target: Union[Callable, str], server_side=False) -> None:
        """Open a new page in the browser by exchanging the content of the root page's slot element

        :param target: the target route or builder function
        :param server_side: Defines if the call is made from the server side and should be pushed to the browser
        history"""
        if isinstance(target, Callable):
            target = {v: k for k, v in self.routes.items()}[target]
            builder = target
        else:
            if target not in self.routes:
                return
            builder = self.routes[target]

        page_config = Client.page_configs.get(builder, None)
        if page_config is not None:  # if page was decorated w/ title, favicon etc.
            title = page_config.title
            ui.run_javascript(f"document.title = '{title if title is not None else core.app.config.title}'")

        if server_side:
            ui.run_javascript(f'window.history.pushState({{page: "{target}"}}, "", "{target}");')

        async def build(content_element) -> None:
            with content_element:
                result = builder()
                if helpers.is_coroutine_function(builder):
                    await result

        content = app.storage.session['__pageContent']
        content.clear()

        background_tasks.create(build(content))
