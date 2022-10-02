import justpy as jp
from nicegui.elements.element import Element
from nicegui.elements.float_element import FloatElement
from nicegui.elements.group import Group
from nicegui.elements.value_element import ValueElement

from mixins import ContextMixin, LabelValueGetSetMixin, BindMixin


class Layout(Group):

    def __init__(self, view='hHh lpR fFf', **kwargs):
        """Layout"""
        view = jp.QLayout(view=view, container=False, classes='shadow-2 rounded-borders', **kwargs)
        super().__init__(view)


class Header(Group):

    def __init__(self, **kwargs):
        """Header"""
        view = jp.QHeader(elevated=True, classes='bg-dark', **kwargs)
        super().__init__(view)


class PageContainer(Group):

    def __init__(self, **kwargs):
        """PageContainer"""
        view = jp.QPageContainer(**kwargs)
        super().__init__(view)


class Footer(Group):

    def __init__(self, **kwargs):
        """Footer"""
        view = jp.QFooter(elevated=True, classes='bg-grey-8 text-white', **kwargs)
        super().__init__(view)


class Div(Element, ContextMixin):

    def __init__(self, **kwargs):
        """QDiv Container"""
        view = jp.QDiv(temp=False, **kwargs)
        super().__init__(view)


@jp.parse_dict
class QBadge(jp.QBadge, LabelValueGetSetMixin):
    pass


class Badge(ValueElement, BindMixin):

    def __init__(self, target_object, target_name='progress_str', **kwargs):
        """QBadge"""
        view = QBadge(color='white', text_color='accent', delete_flag=False, temp=True)
        view.label = 'n/v'  # workaround attribute issues -> any idea?
        super().__init__(view, value='some', on_change=None)
        if target_object:
            self.bind_from(attr='value', target_object=target_object, target_name=target_name)


class LinearProgress(FloatElement, ContextMixin):

    def __init__(self, *, value: float = 0, target_object=None, target_name=None, **kwargs):
        """LinearProgress"""
        view = jp.QLinearProgress(color='bg-grey-2', style="height: 25px;", value=value, temp=False)
        super().__init__(view, value=value, on_change=None, **kwargs)
        if target_object and target_name:
            self.bind_value_from(target_object=target_object, target_name=target_name)
