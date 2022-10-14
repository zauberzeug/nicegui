from typing import Callable, Optional

from addict import Dict
from nicegui.elements.custom_view import CustomView
from nicegui.elements.element import Element
from nicegui.routes import add_dependencies

add_dependencies(__file__)  # automatically serve the .js file with the same name


class CounterView(CustomView):

    def __init__(self, title: str, on_change: Optional[Callable]) -> None:
        super().__init__('counter', title=title, value=0)  # pass props to the Vue component

        self.on_change = on_change
        self.allowed_events = ['onChange']
        self.initialize(temp=False, onChange=self.handle_change)

    def handle_change(self, msg: Dict) -> None:
        if self.on_change is not None:
            self.on_change(msg.value)
        return False  # avoid JustPy's page update


class Counter(Element):

    def __init__(self, title: str, *, on_change: Optional[Callable] = None) -> None:
        super().__init__(CounterView(title, on_change))

    def reset(self) -> None:
        self.view.options.value = 0
        self.update()  # update the view after changing the counter value
