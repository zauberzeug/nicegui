from typing import Optional

from typing_extensions import Literal

from . import globals
from .element import Element
from .elements.mixins.value_element import ValueElement

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


class Header(ValueElement):

    def __init__(self, *,
                 value: bool = True,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False) -> None:
        '''Header

        :param value: whether the header is already opened (default: `True`)
        :param fixed: whether the header should be fixed to the top of the page (default: `True`)
        :param bordered: whether the header should have a border (default: `False`)
        :param elevated: whether the header should have a shadow (default: `False`)
        '''
        with globals.get_client().layout:
            super().__init__(tag='q-header', value=value, on_value_change=None)
        self._classes = ['nicegui-header']
        self._props['bordered'] = bordered
        self._props['elevated'] = elevated
        code = list(self.client.layout._props['view'])
        code[1] = 'H' if fixed else 'h'
        self.client.layout._props['view'] = ''.join(code)

    def toggle(self):
        '''Toggle the header'''
        self.value = not self.value

    def show(self):
        '''Show the header'''
        self.value = True

    def hide(self):
        '''Hide the header'''
        self.value = False


class Drawer(Element):

    def __init__(self,
                 side: DrawerSides, *,
                 value: Optional[bool] = None,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False,
                 top_corner: bool = False,
                 bottom_corner: bool = False) -> None:
        '''Drawer

        :param side: side of the page where the drawer should be placed (`left` or `right`)
        :param value: whether the drawer is already opened (default: `None`, i.e. if layout width is above threshold)
        :param fixed: whether the drawer is fixed or scrolls with the content (default: `True`)
        :param bordered: whether the drawer should have a border (default: `False`)
        :param elevated: whether the drawer should have a shadow (default: `False`)
        :param top_corner: whether the drawer expands into the top corner (default: `False`)
        :param bottom_corner: whether the drawer expands into the bottom corner (default: `False`)
        '''
        with globals.get_client().layout:
            super().__init__('q-drawer')
        if value is None:
            self._props['show-if-above'] = True
        else:
            self._props['model-value'] = value
        self._props['side'] = side
        self._props['bordered'] = bordered
        self._props['elevated'] = elevated
        self._classes = ['nicegui-drawer']
        code = list(self.client.layout._props['view'])
        code[0 if side == 'left' else 2] = side[0].lower() if top_corner else 'h'
        code[4 if side == 'left' else 6] = side[0].upper() if fixed else side[0].lower()
        code[8 if side == 'left' else 10] = side[0].lower() if bottom_corner else 'f'
        self.client.layout._props['view'] = ''.join(code)

    def toggle(self) -> None:
        '''Toggle the drawer'''
        self.run_method('toggle')

    def show(self) -> None:
        '''Show the drawer'''
        self.run_method('show')

    def hide(self) -> None:
        '''Hide the drawer'''
        self.run_method('hide')


class LeftDrawer(Drawer):

    def __init__(self, *,
                 value: Optional[bool] = None,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False,
                 top_corner: bool = False,
                 bottom_corner: bool = False) -> None:
        '''Left drawer

        :param value: whether the drawer is already opened (default: `None`, i.e. if layout width is above threshold)
        :param fixed: whether the drawer is fixed or scrolls with the content (default: `True`)
        :param bordered: whether the drawer should have a border (default: `False`)
        :param elevated: whether the drawer should have a shadow (default: `False`)
        :param top_corner: whether the drawer expands into the top corner (default: `False`)
        :param bottom_corner: whether the drawer expands into the bottom corner (default: `False`)
        '''
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
        '''Right drawer

        :param value: whether the drawer is already opened (default: `None`, i.e. if layout width is above threshold)
        :param fixed: whether the drawer is fixed or scrolls with the content (default: `True`)
        :param bordered: whether the drawer should have a border (default: `False`)
        :param elevated: whether the drawer should have a shadow (default: `False`)
        :param top_corner: whether the drawer expands into the top corner (default: `False`)
        :param bottom_corner: whether the drawer expands into the bottom corner (default: `False`)
        '''
        super().__init__('right',
                         value=value,
                         fixed=fixed,
                         bordered=bordered,
                         elevated=elevated,
                         top_corner=top_corner,
                         bottom_corner=bottom_corner)


class Footer(ValueElement):

    def __init__(self, *,
                 value: bool = True,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False) -> None:
        '''Footer

        :param value: whether the footer is already opened (default: `True`)
        :param fixed: whether the footer is fixed or scrolls with the content (default: `True`)
        :param bordered: whether the footer should have a border (default: `False`)
        :param elevated: whether the footer should have a shadow (default: `False`)
        '''
        with globals.get_client().layout:
            super().__init__(tag='q-footer', value=value, on_value_change=None)
        self.classes('nicegui-footer')
        self._props['bordered'] = bordered
        self._props['elevated'] = elevated
        code = list(self.client.layout._props['view'])
        code[9] = 'F' if fixed else 'f'
        self.client.layout._props['view'] = ''.join(code)

    def toggle(self) -> None:
        '''Toggle the footer'''
        self.value = not self.value

    def show(self) -> None:
        '''Show the footer'''
        self.value = True

    def hide(self) -> None:
        '''Hide the footer'''
        self.value = False


class PageSticky(Element):

    def __init__(self, position: PageStickyPositions = 'bottom-right', x_offset: float = 0, y_offset: float = 0) -> None:
        '''Page sticky

        A sticky element that is always visible at the bottom of the page.

        :param position: position of the sticky element (default: `'bottom-right'`)
        :param x_offset: horizontal offset of the sticky element (default: `0`)
        :param y_offset: vertical offset of the sticky element (default: `0`)
        '''
        super().__init__('q-page-sticky')
        self._props['position'] = position
        self._props['offset'] = [x_offset, y_offset]
