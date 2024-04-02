import inspect
from typing import Callable, Dict, Union

from fastapi.routing import APIRoute

from nicegui import background_tasks, helpers, ui, core


class RouterFrame(ui.element, component='single_page.js'):
    pass


class PageBuilder:
    def __init__(self) -> None:
        pass

    def header(self):
        ui.label("Head")

    def footer(self):
        ui.label("Foot")

    def build(self):
        self.header()
        self.footer()


class SinglePageRouter(PageBuilder):

    def __init__(self, base_path: str = "/") -> None:
        super().__init__()

        self.routes: Dict[str, Callable] = {}
        self.content: ui.element = None
        self.base_path = base_path

        candidates = self.find_api_routes()
        self.find_method_candidates(candidates)

        @ui.page(base_path)
        @ui.page(f'{base_path}' + '{_:path}')  # all other pages
        def root_page():
            self.build()

    def find_api_routes(self) -> list[str]:
        page_routes = []
        removed_routes = []
        for route in core.app.routes:
            if isinstance(route, APIRoute):
                if (route.path.startswith(self.base_path) and
                        route.path != self.base_path and
                        not route.path[len(self.base_path):].startswith("_")):
                    removed_routes.append(route.path)
                    page_routes.append(route)
        for route in page_routes:
            core.app.routes.remove(route)
        return removed_routes

    def find_method_candidates(self, candidates: list[str]):
        src_globals = inspect.stack()[2].frame.f_globals
        for obj in src_globals:
            if isinstance(obj, Callable):  # and name == 'some_page':
                # obj()
                print(obj)

    def add(self, path: str):
        def decorator(func: Callable):
            self.routes[path] = func
            return func

        return decorator

    def open(self, target: Union[Callable, str]) -> None:
        if isinstance(target, str):
            path = target
            builder = self.routes[target]
        else:
            path = {v: k for k, v in self.routes.items()}[target]
            builder = target

        async def build() -> None:
            with self.content:
                ui.run_javascript(f'''
                    if (window.location.pathname !== "{path}") {{
                        history.pushState({{page: "{path}"}}, "", "{path}");
                    }}
                ''')
                result = builder()
                if helpers.is_coroutine_function(builder):
                    await result

        self.content.clear()
        background_tasks.create(build())

    def frame(self) -> ui.element:
        self.content = RouterFrame().on('open', lambda e: self.open(e.args))
        return self.content
