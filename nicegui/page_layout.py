from typing import Literal, Optional

from .context import context
from .element import Element
from .elements.mixins.value_element import ValueElement
from .functions.html import add_body_html

DrawerSides = Literal['left', 'right']

PageStickyPositions = Literal[
    'top-right',
    'top-left',
    'bottom-right',
    'bottom-left',
    'top',
    'right',
    'bottom',
    'left',
]


class Header(ValueElement, default_classes='nicegui-header'):

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
        _check_current_slot(self)
        with context.client.layout:
            super().__init__(tag='q-header', value=value, on_value_change=None)
        self._props['bordered'] = bordered
        self._props['elevated'] = elevated
        if wrap:
            self._classes.append('wrap')
        code = list(self.client.layout.props['view'])
        code[1] = 'H' if fixed else 'h'
        self.client.layout.props['view'] = ''.join(code)

        self.move(target_index=0)

        if add_scroll_padding:
            add_body_html(f'''
                <script>
                    window.onload = () => {{
                        const header = getHtmlElement({self.id});
                        new ResizeObserver(() => {{
                            document.documentElement.style.scrollPaddingTop = `${{header.offsetHeight}}px`;
                        }}).observe(header);
                    }};
                </script>
            ''')

    def toggle(self):
        """Toggle the header"""
        self.value = not self.value

    def show(self):
        """Show the header"""
        self.value = True

    def hide(self):
        """Hide the header"""
        self.value = False


class Drawer(Element, default_classes='nicegui-drawer'):

    def __init__(self,
                 side: DrawerSides, *,
                 value: Optional[bool] = None,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False,
                 top_corner: bool = False,
                 bottom_corner: bool = False) -> None:
        """Drawer

        This element is based on Quasar's `QDrawer <https://quasar.dev/layout/drawer>`_ component.

        Like other layout elements, a drawer can not be nested inside other elements.

        Note: Depending on the side, the drawer is automatically placed above or below the main page container in the DOM to improve accessibility.
        To change the order, use the `move` method.

        :param side: side of the page where the drawer should be placed (`left` or `right`)
        :param value: whether the drawer is already opened (default: `None`, i.e. if layout width is above threshold)
        :param fixed: whether the drawer is fixed or scrolls with the content (default: `True`)
        :param bordered: whether the drawer should have a border (default: `False`)
        :param elevated: whether the drawer should have a shadow (default: `False`)
        :param top_corner: whether the drawer expands into the top corner (default: `False`)
        :param bottom_corner: whether the drawer expands into the bottom corner (default: `False`)
        """
        _check_current_slot(self)
        with context.client.layout:
            super().__init__('q-drawer')
        if value is None:
            self._props['show-if-above'] = True
        else:
            self._props['model-value'] = value
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

    def toggle(self) -> None:
        """Toggle the drawer"""
        self.run_method('toggle')

    def show(self) -> None:
        """Show the drawer"""
        self.run_method('show')

    def hide(self) -> None:
        """Hide the drawer"""
        self.run_method('hide')


class LeftDrawer(Drawer):

    def __init__(self, *,
                 value: Optional[bool] = None,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False,
                 top_corner: bool = False,
                 bottom_corner: bool = False) -> None:
        """Left drawer

        This element is based on Quasar's `QDrawer <https://quasar.dev/layout/drawer>`_ component.

        Like other layout elements, the left drawer can not be nested inside other elements.

        Note: The left drawer is automatically placed above the main page container in the DOM to improve accessibility.
        To change the order, use the `move` method.

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

    def __init__(self, *,
                 value: Optional[bool] = None,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False,
                 top_corner: bool = False,
                 bottom_corner: bool = False) -> None:
        """Right drawer

        This element is based on Quasar's `QDrawer <https://quasar.dev/layout/drawer>`_ component.

        Like other layout elements, the right drawer can not be nested inside other elements.

        Note: The right drawer is automatically placed below the main page container in the DOM to improve accessibility.
        To change the order, use the `move` method.

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


class Footer(ValueElement, default_classes='nicegui-footer'):

    def __init__(self, *,
                 value: bool = True,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False,
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
        _check_current_slot(self)
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


class PageSticky(Element):

    def __init__(self,
                 position: PageStickyPositions = 'bottom-right',
                 x_offset: float = 0,
                 y_offset: float = 0,
                 *,
                 expand: bool = False) -> None:
        """Page sticky

        This element is based on Quasar's `QPageSticky <https://quasar.dev/layout/page-sticky>`_ component.

        :param position: position on the screen (default: "bottom-right")
        :param x_offset: horizontal offset (default: 0)
        :param y_offset: vertical offset (default: 0)
        :param expand: whether to fully expand instead of shrinking to fit the content (default: ``False``)
        """
        super().__init__('q-page-sticky')
        self._props['position'] = position
        self._props['offset'] = [x_offset, y_offset]
        if expand:
            self._props['expand'] = True


def _check_current_slot(element: Element) -> None:
    parent = context.slot.parent
    if parent != parent.client.content:
        raise RuntimeError(f'Found top level layout element "{element.__class__.__name__}" inside element "{parent.__class__.__name__}". '
                           'Top level layout elements can not be nested but must be direct children of the page content.')
