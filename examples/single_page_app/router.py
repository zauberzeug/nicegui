from typing import Callable

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

    def open(self, func: Callable):
        path = {v: k for k, v in self.routes.items()}[func]
        self.content.clear()

        async def build():
            with self.content:
                cmd = f'history.pushState({{page: "{path}"}}, "", "{path}")'
                print(cmd, flush=True)
                await ui.run_javascript(cmd, respond=False)
                await func()
        background_tasks.create(build())

    def frame(self):
        self.content = ui.element('router_frame')
        with self.content:
            ui.label('Loading...').classes('text-2xl')
        return self.content
