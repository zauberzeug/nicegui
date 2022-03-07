import justpy as jp
from ..binding import bind_from, bind_to, BindableProperty
from ..globals import view_stack, page_stack

class Element:
    visible = BindableProperty(
        on_change=lambda sender, visible: (sender.view.remove_class if visible else sender.view.set_class)('hidden'))

    def __init__(self,
                 view: jp.HTMLBaseComponent,
                 ):
        self.parent_view = view_stack[-1]
        self.parent_view.add(view)
        self.view = view
        self.page = page_stack[-1]
        self.view.add_page(self.page)

        self.visible = True

    def bind_visibility_to(self, target_object, target_name, forward=lambda x: x):
        bind_to(self, 'visible', target_object, target_name, forward=forward)
        return self

    def bind_visibility_from(self, target_object, target_name, backward=lambda x: x, *, value=None):
        if value is not None:
            def backward(x): return x == value

        bind_from(self, 'visible', target_object, target_name, backward=backward)
        return self

    def bind_visibility(self, target_object, target_name, forward=lambda x: x, backward=None, *, value=None):
        if value is not None:
            def backward(x): return x == value

        bind_from(self, 'visible', target_object, target_name, backward=backward)
        bind_to(self, 'visible', target_object, target_name, forward=forward)
        return self

    def classes(self, add: str = None, *, remove: str = None, replace: str = None):
        '''HTML classes to modify the look of the element.
        Every class in the `remove` parameter will be removed from the element.
        Classes are seperated with a blank space.
        This can be helpful if the predefined classes by NiceGUI are not wanted in a particular styling.
        '''
        class_list = [] if replace is not None else self.view.classes.split()
        class_list = [c for c in class_list if c not in (remove or '')]
        class_list += (add or '').split()
        class_list += (replace or '').split()
        self.view.classes = ' '.join(class_list)

        return self

    def style(self, add: str = None, *, remove: str = None, replace: str = None):
        '''CSS style sheet definitions to modify the look of the element.
        Every style in the `remove` parameter will be removed from the element.
        Styles are seperated with a semicolon.
        This can be helpful if the predefined style sheet definitions by NiceGUI are not wanted in a particular styling.
        '''
        style_list = [] if replace is not None else self.view.style.split(';')
        style_list = [c for c in style_list if c not in (remove or '').split(';')]
        style_list += (add or '').split(';')
        style_list += (replace or '').split(';')
        self.view.style = ';'.join(style_list)

        return self

    def props(self, add: str = None, *, remove: str = None, replace: str = None):
        '''Quasar props https://quasar.dev/vue-components/button#design to modify the look of the element.
        Boolean props will automatically activated if they appear in the list of the `add` property.
        Props are seperated with a blank space.
        Every prop passed to the `remove` parameter will be removed from the element.
        This can be helpful if the predefined props by NiceGUI are not wanted in a particular styling.
        '''
        for prop in (remove or '').split() + (replace or '').split():
            setattr(self.view, prop.split('=')[0], None)

        for prop in (add or '').split() + (replace or '').split():
            if '=' in prop:
                setattr(self.view, *prop.split('='))
            else:
                setattr(self.view, prop, True)

        return self
