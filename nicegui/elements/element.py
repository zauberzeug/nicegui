import justpy as jp
from binding.binding import BindableProperty

class Element:

    wp: None
    view_stack = []

    visible = BindableProperty

    def __init__(self,
                 view: jp.HTMLBaseComponent,
                 ):

        self.parent_view = self.view_stack[-1]
        self.parent_view.add(view)
        view.add_page(self.wp)
        self.view = view

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

    def classes(self, add: str = '', *, remove: str = '', replace: str = ''):

        class_list = [] if replace else self.view.classes.split()
        class_list = [c for c in class_list if c not in remove]
        class_list += add.split()
        class_list += replace.split()
        self.view.classes = ' '.join(class_list)

        return self

    def style(self, add: str = '', *, remove: str = '', replace: str = ''):

        style_list = [] if replace else self.view.style.split(';')
        style_list = [c for c in style_list if c not in remove.split(';')]
        style_list += add.split(';')
        style_list += replace.split(';')
        self.view.style = ';'.join(style_list)

        return self

    def props(self, add: str = '', *, remove: str = '', replace: str = ''):

        for prop in remove.split() + replace.split():
            setattr(self.view, prop.split('=')[0], None)

        for prop in add.split() + replace.split():
            if '=' in prop:
                setattr(self.view, *prop.split('='))
            else:
                setattr(self.view, prop, True)

        return self
