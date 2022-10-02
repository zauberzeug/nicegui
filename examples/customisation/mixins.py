from nicegui import binding

from nicegui.globals import get_view_stack  # type: ignore


class ContextMixin:
    """
    Mixin providing a context manager for additional components.
    copied from nicegui.elements.group.Group
    """

    def __enter__(self):
        self._child_count_on_enter = len(self.view)
        get_view_stack().append(self.view)
        return self

    def __exit__(self, *_):
        get_view_stack().pop()
        if self._child_count_on_enter != len(self.view):
            self.update()


class BindMixin:
    """
    Mixin providing bind methods.
    derived from nicegui.elements.value_element.ValueElement
    """

    def bind_from(self, target_object, target_name, *, attr: str = 'value', backward=lambda x: x):
        binding.bind_from(self, attr, target_object, target_name, backward=backward)

    def bind_to(self, target_object, target_name, *, attr: str = 'value', forward=lambda x: x):
        binding.bind_to(self, attr, target_object, target_name, forward=forward)
        return self

    def bind(self, target_object, target_name, *, attr: str = 'value', forward=lambda x: x, backward=lambda x: x):
        self.bind_from(target_object, target_name, attr=attr, backward=backward)
        self.bind_to(target_object, target_name, attr=attr, forward=forward)
        return self


class LabelValueGetSetMixin:
    @property
    def value(self):
        return self.label

    @value.setter
    def value(self, value):
        self.label = value
