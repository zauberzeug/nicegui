from .custom_view import CustomView
from .element import Element

class CustomExampleView(CustomView):

    def __init__(self, on_change):

        super().__init__('custom_example', __file__, value=0)

        self.on_change = on_change
        self.allowed_events = ['onAdd']
        self.initialize(temp=False, onAdd=self.handle_add)

    def handle_add(self, msg):

        self.options.value += msg.number
        if self.on_change is not None:
            self.on_change(self.options.value)

class CustomExample(Element):

    def __init__(self, *, on_change=None):

        super().__init__(CustomExampleView(on_change))

    def add(self, number: str):

        self.view.options.value += number
        self.view.on_change(self.view.options.value)
