from . import globals
from .element import Element


class Header(Element):

    def __init__(self, fixed: bool = True) -> None:
        with globals.get_client().layout:
            super().__init__('q-header')
        self.classes('q-pa-md row items-start gap-4')
        code = list(self.client.layout._props['view'])
        code[1] = 'H' if fixed else 'h'
        self.client.layout._props['view'] = ''.join(code)


class Drawer(Element):

    def __init__(self, side: str, *, fixed: bool = True, top_corner: bool = False, bottom_corner: bool = False) -> None:
        assert side in {'left', 'right'}
        with globals.get_client().layout:
            super().__init__('q-drawer')
        self._props['show-if-above'] = True
        self._props['side'] = side
        self._classes = ['q-pa-md']
        code = list(self.client.layout._props['view'])
        code[0 if side == 'left' else 2] = side[0].lower() if top_corner else 'h'
        code[4 if side == 'left' else 6] = side[0].upper() if fixed else side[0].lower()
        code[8 if side == 'left' else 10] = side[0].lower() if bottom_corner else 'f'
        self.client.layout._props['view'] = ''.join(code)


class LeftDrawer(Drawer):

    def __init__(self, fixed: bool = True, top_corner: bool = False, bottom_corner: bool = False) -> None:
        super().__init__('left', fixed=fixed, top_corner=top_corner, bottom_corner=bottom_corner)


class RightDrawer(Drawer):

    def __init__(self, fixed: bool = True, top_corner: bool = False, bottom_corner: bool = False) -> None:
        super().__init__('right', fixed=fixed, top_corner=top_corner, bottom_corner=bottom_corner)


class Footer(Element):

    def __init__(self, fixed: bool = True) -> None:
        with globals.get_client().layout:
            super().__init__('q-footer')
        self.classes('q-pa-md row items-start gap-4')
        code = list(self.client.layout._props['view'])
        code[9] = 'F' if fixed else 'f'
        self.client.layout._props['view'] = ''.join(code)


class PageSticky(Element):

    def __init__(self) -> None:
        super().__init__('q-page-sticky')
