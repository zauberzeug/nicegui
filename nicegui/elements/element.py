import justpy as jp
from enum import Enum
from binding.binding import BindableProperty
from ..globals import view_stack, page_stack

class Element:
    visible = BindableProperty

    def __init__(self,
                 view: jp.HTMLBaseComponent,
                 ):
        self.parent_view = view_stack[-1]
        self.parent_view.add(view)
        self.view = view
        self.page = page_stack[-1]
        self.view.add_page(self.page)

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

    def bind_visibility_from(self, target, backward=lambda x: x, *, value=None):
        if value is not None:
            def backward(x): return x == value

        self.visible.bind_from(target, backward=backward, nesting=1)
        return self

    def bind_visibility(self, target, forward=lambda x: x, backward=None, *, value=None):
        if value is not None:
            def backward(x): return x == value

        self.visible.bind(target, forward=forward, backward=backward, nesting=1)
        return self

    def classes(self, add: str = '', *, remove: str = '', replace: str = ''):
        '''HTML classes to modify the look of the element.
        Every class in the `remove` parameter will be removed from the element.
        Classes are seperated with a blank space.
        This can be helpful if the predefined classes by NiceGUI are not wanted in a particular styling.
        '''
        class_list = [] if replace else self.view.classes.split()
        class_list = [c for c in class_list if c not in remove]
        class_list += add.split()
        class_list += replace.split()
        self.view.classes = ' '.join(class_list)

        return self

    def style(self, add: str = '', *, remove: str = '', replace: str = ''):
        '''CSS style sheet definitions to modify the look of the element.
        Every style in the `remove` parameter will be removed from the element.
        Styles are seperated with a semicolon.
        This can be helpful if the predefined style sheet definitions by NiceGUI are not wanted in a particular styling.
        '''
        style_list = [] if replace else self.view.style.split(';')
        style_list = [c for c in style_list if c not in remove.split(';')]
        style_list += add.split(';')
        style_list += replace.split(';')
        self.view.style = ';'.join(style_list)

        return self

    def props(self, add: str = '', *, remove: str = '', replace: str = ''):
        '''Quasar props https://quasar.dev/vue-components/button#design to modify the look of the element.
        Boolean props will automatically activated if they appear in the list of the `add` property.
        Props are seperated with a blank space.
        Every prop passed to the `remove` parameter will be removed from the element.
        This can be helpful if the predefined props by NiceGUI are not wanted in a particular styling.
        '''
        for prop in remove.split() + replace.split():
            setattr(self.view, prop.split('=')[0], None)

        for prop in add.split() + replace.split():
            if '=' in prop:
                setattr(self.view, *prop.split('='))
            else:
                setattr(self.view, prop, True)

        return self

class Design(Enum):
    default = 1
    plain = 2
