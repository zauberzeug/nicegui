from typing import Awaitable, Callable, Union

from nicegui import background_tasks, ui
from nicegui.dependencies import register_component
from nicegui.element import Element

register_component('router_frame', __file__, 'router_frame.js')


class Router():

    def __init__(self) -> None:
        self.routes: dict[str, Callable] = {}
        self.content: Element = None

    def add(self, path: str):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

    def open(self, target: Union[Callable, Awaitable, str]):
        if isinstance(target, str):
            path = target
            builder = self.routes[target]
        else:
            path = {v: k for k, v in self.routes.items()}[target]
            builder = target
        self.content.clear()

        async def build():
            with self.content:
                await ui.run_javascript(f'history.pushState({{page: "{path}"}}, "", "{path}")', respond=False)
                await builder()
        background_tasks.create(build())

    def frame(self):
        self.content = ui.element('router_frame').on('open', lambda msg: self.open(msg['args']))
        return self.content
