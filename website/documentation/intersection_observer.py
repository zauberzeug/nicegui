from typing import Callable

from nicegui.element import Element
from nicegui.events import UiEventArguments, handle_event


class IntersectionObserver(Element, component='intersection_observer.js'):

    def __init__(self, *, on_intersection: Callable) -> None:
        super().__init__()
        self.on_intersection = on_intersection
        self.active = True
        self.on('intersection', self.handle_intersection, [])

    def handle_intersection(self, _) -> None:
        self.run_method('stop')
        if self.active:
            handle_event(self.on_intersection, UiEventArguments(sender=self, client=self.client))
            self.active = False
