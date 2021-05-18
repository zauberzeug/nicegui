import justpy as jp
from binding.binding import BindableProperty

class Element:

    wp: None
    view_stack = []

    visible = BindableProperty

    def __init__(self, view: jp.HTMLBaseComponent, design: str = '', classes: str = ''):

        for word in design.split():
            if '=' in word:
                setattr(view, *word.split('='))
            else:
                setattr(view, word, True)

        self.parent_view = self.view_stack[-1]
        self.parent_view.add(view)
        view.add_page(self.wp)
        self.view = view
        self.view.classes += ' ' + classes

        self.visible = True

    @property
    def visible(self):

        return self.visible_

    @visible.setter
    def visible(self, visible: bool):

        self.visible_ = visible
        (self.view.remove_class if self.visible_ else self.view.set_class)('hidden')

    def bind_visibility_to(self, target, forward=lambda x: x):

        self.visible.bind_to(target, forward=forward, nesting=1)
        return self

    def bind_visibility_from(self, target, backward=lambda x: x):

        self.visible.bind_from(target, backward=backward, nesting=1)
        return self

    def bind_visibility(self, target, forward=lambda x: x, backward=lambda x: x):

        self.visible.bind(target, forward=forward, backward=backward, nesting=1)
        return self

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
