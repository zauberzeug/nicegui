from typing import Callable

from nicegui.element import Element
from nicegui.events import UiEventArguments, handle_event


class IntersectionObserver(Element, component='intersection_observer.js'):
    """
    IntersectionObserver is a class that allows you to observe when an element enters or exits the viewport.

    Args:
        on_intersection (Callable): A callback function that will be called when the element intersects with the viewport.

    Attributes:
        active (bool): Indicates whether the IntersectionObserver is currently active.

    Example:
        def handle_intersection():
            print("Element intersected with the viewport")

        observer = IntersectionObserver(on_intersection=handle_intersection)
        observer.observe(element)
    """

    def __init__(self, *, on_intersection: Callable) -> None:
        super().__init__()
        self.on_intersection = on_intersection
        self.active = True
        self.on('intersection', self.handle_intersection, [])

    def handle_intersection(self, _) -> None:
        """
        Handles the intersection event and triggers the on_intersection callback.

        Args:
            _: Unused argument.

        Returns:
            None
        """
        self.run_method('stop')
        if self.active:
            handle_event(self.on_intersection, UiEventArguments(sender=self, client=self.client))
            self.active = False
