from pathlib import Path
from typing import Callable

from nicegui.dependencies import register_vue_component
from nicegui.element import Element
from nicegui.events import EventArguments, handle_event

register_vue_component(name='intersection_observer', path=Path(__file__).parent / 'intersection_observer.js')


class IntersectionObserver(Element):

    def __init__(self, *, on_intersection: Callable) -> None:
        super().__init__('intersection_observer')
        self.on_intersection = on_intersection
        self.active = True
        self.on('intersection', self.handle_intersection)
        self.use_component('intersection_observer')

    def handle_intersection(self, _) -> None:
        self.run_method('stop')
        if self.active:
            handle_event(self.on_intersection, EventArguments(sender=self, client=self.client))
            self.active = False
