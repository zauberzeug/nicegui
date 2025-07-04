from ..context import context
from ..helpers import require_top_level_layout
from .mixins.value_element import ValueElement


class Header(ValueElement, component='header.js', default_classes='nicegui-header'):

    def __init__(self, *,
                 value: bool = True,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False,
                 wrap: bool = True,
                 add_scroll_padding: bool = True,
                 ) -> None:
        """Header

        This element is based on Quasar's `QHeader <https://quasar.dev/layout/header-and-footer#qheader-api>`_ component.

        Like other layout elements, the header can not be nested inside other elements.

        Note: The header is automatically placed above other layout elements in the DOM to improve accessibility.
        To change the order, use the `move` method.

        :param value: whether the header is already opened (default: `True`)
        :param fixed: whether the header should be fixed to the top of the page (default: `True`)
        :param bordered: whether the header should have a border (default: `False`)
        :param elevated: whether the header should have a shadow (default: `False`)
        :param wrap: whether the header should wrap its content (default: `True`)
        :param add_scroll_padding: whether to automatically prevent link targets from being hidden behind the header (default: `True`)
        """
        require_top_level_layout(self)
        with context.client.layout:
            super().__init__(value=value, on_value_change=None)
        self._props['bordered'] = bordered
        self._props['elevated'] = elevated
        self._props['add_scroll_padding'] = add_scroll_padding
        if wrap:
            self._classes.append('wrap')
        code = list(self.client.layout.props['view'])
        code[1] = 'H' if fixed else 'h'
        self.client.layout.props['view'] = ''.join(code)

        self.move(target_index=0)

    def toggle(self):
        """Toggle the header"""
        self.value = not self.value

    def show(self):
        """Show the header"""
        self.value = True

    def hide(self):
        """Hide the header"""
        self.value = False
