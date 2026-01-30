from typing import Literal

from ..context import context
from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..helpers import require_top_level_layout
from .mixins.value_element import ValueElement

DrawerSides = Literal['left', 'right']


class Drawer(ValueElement, default_classes='nicegui-drawer'):

    @resolve_defaults
    def __init__(self,
                 side: DrawerSides, *,
                 value: bool | None = DEFAULT_PROPS['model-value'] | None,
                 fixed: bool = True,
                 bordered: bool = DEFAULT_PROP | False,
                 elevated: bool = DEFAULT_PROP | False,
                 top_corner: bool = False,
                 bottom_corner: bool = False) -> None:
        """Drawer

        This element is based on Quasar's `QDrawer <https://quasar.dev/layout/drawer>`_ component.

        Like other layout elements, a drawer can not be nested inside other elements.

        Note: Depending on the side, the drawer is automatically placed above or below the main page container in the DOM to improve accessibility.
        To change the order, use the `move` method.

        A value of ``None`` will automatically open or close the drawer depending on the current layout width (breakpoint: >=1024 px).
        The value will be requested from the client when the websocket connection is established.

        :param side: side of the page where the drawer should be placed (`left` or `right`)
        :param value: whether the drawer is already opened (default: `None`, i.e. if layout width is above threshold)
        :param fixed: whether the drawer is fixed or scrolls with the content (default: `True`)
        :param bordered: whether the drawer should have a border (default: `False`)
        :param elevated: whether the drawer should have a shadow (default: `False`)
        :param top_corner: whether the drawer expands into the top corner (default: `False`)
        :param bottom_corner: whether the drawer expands into the bottom corner (default: `False`)
        """
        require_top_level_layout(self)
        with context.client.layout:
            super().__init__(tag='q-drawer', value=value, on_value_change=None)
        self._props['show-if-above'] = value is None
        self._props['side'] = side
        self._props['bordered'] = bordered
        self._props['elevated'] = elevated
        code = list(self.client.layout.props['view'])
        code[0 if side == 'left' else 2] = side[0].lower() if top_corner else 'h'
        code[4 if side == 'left' else 6] = side[0].upper() if fixed else side[0].lower()
        code[8 if side == 'left' else 10] = side[0].lower() if bottom_corner else 'f'
        self.client.layout.props['view'] = ''.join(code)

        page_container_index = self.client.layout.default_slot.children.index(self.client.page_container)
        self.move(target_index=page_container_index if side == 'left' else page_container_index + 1)

        if value is None:
            async def _request_value() -> None:
                self.value = await context.client.run_javascript(
                    f'!getHtmlElement({self.id}).parentElement.classList.contains("q-layout--prevent-focus")  // __IS_DRAWER_OPEN__'
                )
            self.client.on_connect(_request_value)

    def toggle(self) -> None:
        """Toggle the drawer"""
        if self.value is None:
            self.run_method('toggle')
        else:
            self.value = not self.value

    def show(self) -> None:
        """Show the drawer"""
        self.value = True

    def hide(self) -> None:
        """Hide the drawer"""
        self.value = False

    def _handle_value_change(self, value: bool) -> None:
        super()._handle_value_change(value)
        self._props['show-if-above'] = value is None


class LeftDrawer(Drawer):

    @resolve_defaults
    def __init__(self, *,
                 value: bool | None = DEFAULT_PROPS['model-value'] | None,
                 fixed: bool = True,
                 bordered: bool = DEFAULT_PROP | False,
                 elevated: bool = DEFAULT_PROP | False,
                 top_corner: bool = False,
                 bottom_corner: bool = False) -> None:
        """Left drawer

        This element is based on Quasar's `QDrawer <https://quasar.dev/layout/drawer>`_ component.

        Like other layout elements, the left drawer can not be nested inside other elements.

        Note: The left drawer is automatically placed above the main page container in the DOM to improve accessibility.
        To change the order, use the `move` method.

        A value of ``None`` will automatically open or close the drawer depending on the current layout width (breakpoint: >=1024 px).
        The value will be requested from the client when the websocket connection is established.

        :param value: whether the drawer is already opened (default: `None`, i.e. if layout width is above threshold)
        :param fixed: whether the drawer is fixed or scrolls with the content (default: `True`)
        :param bordered: whether the drawer should have a border (default: `False`)
        :param elevated: whether the drawer should have a shadow (default: `False`)
        :param top_corner: whether the drawer expands into the top corner (default: `False`)
        :param bottom_corner: whether the drawer expands into the bottom corner (default: `False`)
        """
        super().__init__('left',
                         value=value,
                         fixed=fixed,
                         bordered=bordered,
                         elevated=elevated,
                         top_corner=top_corner,
                         bottom_corner=bottom_corner)


class RightDrawer(Drawer):

    @resolve_defaults
    def __init__(self, *,
                 value: bool | None = DEFAULT_PROPS['model-value'] | None,
                 fixed: bool = True,
                 bordered: bool = DEFAULT_PROP | False,
                 elevated: bool = DEFAULT_PROP | False,
                 top_corner: bool = False,
                 bottom_corner: bool = False) -> None:
        """Right drawer

        This element is based on Quasar's `QDrawer <https://quasar.dev/layout/drawer>`_ component.

        Like other layout elements, the right drawer can not be nested inside other elements.

        Note: The right drawer is automatically placed below the main page container in the DOM to improve accessibility.
        To change the order, use the `move` method.

        A value of ``None`` will automatically open or close the drawer depending on the current layout width (breakpoint: >=1024 px).
        The value will be requested from the client when the websocket connection is established.

        :param value: whether the drawer is already opened (default: `None`, i.e. if layout width is above threshold)
        :param fixed: whether the drawer is fixed or scrolls with the content (default: `True`)
        :param bordered: whether the drawer should have a border (default: `False`)
        :param elevated: whether the drawer should have a shadow (default: `False`)
        :param top_corner: whether the drawer expands into the top corner (default: `False`)
        :param bottom_corner: whether the drawer expands into the bottom corner (default: `False`)
        """
        super().__init__('right',
                         value=value,
                         fixed=fixed,
                         bordered=bordered,
                         elevated=elevated,
                         top_corner=top_corner,
                         bottom_corner=bottom_corner)
