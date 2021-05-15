import justpy as jp
from ..binding import Binding

class Element:

    wp: None
    view_stack = []
    all_bindings = []

    def __init__(self, view: jp.HTMLBaseComponent, design: str):

        for word in design.split():
            if '=' in word:
                setattr(view, *word.split('='))
            else:
                setattr(view, word, True)

        self.parent_view = self.view_stack[-1]
        self.parent_view.add(view)
        view.add_page(self.wp)
        self.view = view

        self.visible = True

        self.bindings = []

    @property
    def visible(self):

        return self.visible_

    @visible.setter
    def visible(self, visible: bool):

        self.visible_ = visible
        self.view.set_class('visible' if visible else 'invisible')

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
        return self
