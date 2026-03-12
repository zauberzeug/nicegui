from collections.abc import Callable

from nicegui import ui


class IntersectionObserver(ui.element, component='intersection_observer.js'):

    def __init__(self, on_intersection: Callable) -> None:
        super().__init__()
        self.on('intersection', on_intersection)
