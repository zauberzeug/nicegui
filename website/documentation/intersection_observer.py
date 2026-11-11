from collections.abc import Callable

from nicegui import helpers, ui


class IntersectionObserver(ui.element, component='intersection_observer.js'):

    def __init__(self, on_intersection: Callable) -> None:
        super().__init__()

        async def handle_intersection() -> None:
            self.delete()  # ensure the event fires only once, even if the client remounts the component
            result = on_intersection()
            if helpers.should_await(result):
                await result
        self.on('intersection', handle_intersection)
