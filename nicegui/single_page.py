import asyncio
import inspect
from typing import Callable, Dict, Union

from fastapi.routing import APIRoute

from nicegui import background_tasks, helpers, ui, core, Client, app
from nicegui.app import AppConfig


class RouterFrame(ui.element, component='single_page.js'):
    def __init__(self, base_path: str):
        super().__init__()
        self._props["base_path"] = base_path


class SinglePageRouter:

    def __init__(self, path: str, **kwargs) -> None:
        super().__init__()

        self.routes: Dict[str, Callable] = {}
        # async access lock
        self.base_path = path
        self.find_api_routes()

        @ui.page(path, **kwargs)
        @ui.page(f'{path}' + '{_:path}', **kwargs)  # all other pages
        async def root_page(client: Client):
            await client.connected()
            if app.storage.session.get('__pageContent', None) is None:
                content: Union[ui.element, None] = RouterFrame(self.base_path).on('open', lambda e: self.open(e.args))
                app.storage.session['__pageContent'] = content

    def find_api_routes(self):
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

    def add(self, path: str):
        def decorator(func: Callable):
            self.routes[path] = func
            return func

        return decorator

    def open(self, target: Union[Callable, str], server_side=False) -> None:
        if isinstance(target, Callable):
            target = {v: k for k, v in self.routes.items()}[target]
            builder = target
        else:
            if target not in self.routes:
                return
            builder = self.routes[target]

        if "__ng_page" in builder.__dict__:
            new_page = builder.__dict__["__ng_page"]
            title = new_page.title
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
