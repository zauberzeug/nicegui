from typing import List

from . import globals
from .elements.element import Element
from .task_logger import create_task


def update(self, *elements: List[Element]) -> None:
    if not (globals.loop and globals.loop.is_running()):
        return
    for element in elements:
        create_task(element.view.update())
