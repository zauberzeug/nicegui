from ..context import context
from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..helpers import require_top_level_layout
from .mixins.value_element import ValueElement


class Footer(ValueElement, default_classes='nicegui-footer'):

    @resolve_defaults
    def __init__(self, *,
                 value: bool = DEFAULT_PROPS['model-value'] | True,
                 fixed: bool = True,
                 bordered: bool = DEFAULT_PROP | False,
                 elevated: bool = DEFAULT_PROP | False,
                 wrap: bool = True,
                 ) -> None:
        """Footer

        This element is based on Quasar's `QFooter <https://quasar.dev/layout/header-and-footer#qfooter-api>`_ component.

        Like other layout elements, the footer can not be nested inside other elements.

        Note: The footer is automatically placed below other layout elements in the DOM to improve accessibility.
        To change the order, use the `move` method.

        :param value: whether the footer is already opened (default: `True`)
        :param fixed: whether the footer is fixed or scrolls with the content (default: `True`)
        :param bordered: whether the footer should have a border (default: `False`)
        :param elevated: whether the footer should have a shadow (default: `False`)
        :param wrap: whether the footer should wrap its content (default: `True`)
        """
        require_top_level_layout(self)
        with context.client.layout:
            super().__init__(tag='q-footer', value=value, on_value_change=None)
        self._props['bordered'] = bordered
        self._props['elevated'] = elevated
        if wrap:
            self._classes.append('wrap')
        code = list(self.client.layout.props['view'])
        code[9] = 'F' if fixed else 'f'
        self.client.layout.props['view'] = ''.join(code)

        self.move(target_index=-1)

    def toggle(self) -> None:
        """Toggle the footer"""
        self.value = not self.value

    def show(self) -> None:
        """Show the footer"""
        self.value = True

    def hide(self) -> None:
        """Hide the footer"""
        self.value = False
