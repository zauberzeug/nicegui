from typing import Awaitable, Callable, Dict, Union

from nicegui import background_tasks, ui


class RouterFrame(ui.element, component='router_frame.js'):
    pass


class Router():

    def __init__(self, route_not_found: Callable = None) -> None:
        self.routes: Dict[str, Callable] = {}
        self.content: ui.element = None
        self.paths: list = []
        self.route_not_found = route_not_found if route_not_found else lambda: ui.label("Route not found")

    def add(self, path: str):
        def decorator(func: Callable):
            self.routes[path] = func
            return func
        return decorator

    def open(self, target: Union[Callable, str]) -> None:
        if isinstance(target, str):
            path = target
            self.paths = target.split('/')[1:]
            combine = f'/{self.paths[0]}'
            builder = self.routes[combine] if combine in self.routes else self.route_not_found
        else:
            path = {v: k for k, v in self.routes.items()}[target]
            builder = target

        async def build() -> None:
            with self.content:
                await ui.run_javascript(f'''
                    if (window.location.pathname !== "{path}") {{
                        history.pushState({{page: "{path}"}}, "", "{path}");
                    }}
                ''', respond=False)
                result = builder()
                if isinstance(result, Awaitable):
                    await result
        self.content.clear()
        background_tasks.create(build())

    def frame(self) -> ui.element:
        self.content = RouterFrame().on('open', lambda e: self.open(e.args))
        return self.content
