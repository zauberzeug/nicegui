from pathlib import Path
from typing import Awaitable, Callable, Dict, Union

from nicegui import background_tasks, ui
from nicegui.dependencies import register_vue_component

register_vue_component(name='router_frame', path=Path(__file__).parent.joinpath('router_frame.js'))


class Router():

    def __init__(self) -> None:
        self.routes: Dict[str, Callable] = {}
        self.content: ui.element = None

    def add(self, path: str):
        def decorator(func: Callable):
            self.routes[path] = func
            return func
        return decorator

    def open(self, target: Union[Callable, str]):
        if isinstance(target, str):
            path = target
            builder = self.routes[target]
        else:
            path = {v: k for k, v in self.routes.items()}[target]
            builder = target

        async def build():
            with self.content:
                await ui.run_javascript(f'history.pushState({{page: "{path}"}}, "", "{path}")', respond=False)
                result = builder()
                if isinstance(result, Awaitable):
                    await result
        self.content.clear()
        background_tasks.create(build())

    def frame(self) -> ui.element:
        self.content = ui.element('router_frame').on('open', lambda msg: self.open(msg['args'])).use_component('router_frame')
        return self.content
