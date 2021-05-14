import justpy as jp
from ..binding import Binding

class Element:

    wp: None
    view_stack = []
    all_bindings = []

    def __init__(self, view: jp.HTMLBaseComponent):

        self.parent_view = self.view_stack[-1]
        self.parent_view.add(view)
        view.add_page(self.wp)
        self.view = view
        self.bindings = []

    def set_classes(self, classes: str):

        self.view.classes = classes
        return self

    def add_classes(self, classes: str):

        self.view.classes += ' ' + classes
        return self

    def set_style(self, style: str):

        self.view.style = style
        return self

    def add_style(self, style: str):

        self.view.style += ' ' + style
        return self

    def bind(self, attribute, model, model_attribute):

        binding = Binding(self, attribute, model, model_attribute)
        self.bindings.append(binding)
        Binding.all_bindings.append(binding)
