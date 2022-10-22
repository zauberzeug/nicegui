import justpy as jp

from .elements.group import Group
from .page import find_parent_page


class Header(Group):

    def __init__(self, fixed: bool = True) -> None:
        view = jp.QHeader(classes='q-pa-md row items-start gap-4', temp=False)
        super().__init__(view)
        code = list(find_parent_page().layout.view)
        code[1] = 'H' if fixed else 'h'
        find_parent_page().layout.view = ''.join(code)


class Drawer(Group):

    def __init__(self, side: str, *, fixed: bool = True, top_corner: bool = False, bottom_corner: bool = False) -> None:
        assert side in ['left', 'right']
        view = jp.QDrawer(side=side, content_class='q-pa-md', content_style='', temp=False)
        super().__init__(view)
        code = list(find_parent_page().layout.view)
        code[0 if side == 'left' else 2] = side[0].lower() if top_corner else 'h'
        code[4 if side == 'left' else 6] = side[0].upper() if fixed else side[0].lower()
        code[8 if side == 'left' else 10] = side[0].lower() if bottom_corner else 'f'
        find_parent_page().layout.view = ''.join(code)

    def classes(self, add: str = '', *, replace: str = ''):
        if replace:
            self.view.content_class = replace
        self.view.content_class += f' {add}'
        return self

    def style(self, add: str = '', *, replace: str = ''):
        if replace:
            self.view.content_style = replace
        self.view.content_style += f';{add}'
        return self


class LeftDrawer(Drawer):

    def __init__(self, fixed: bool = True, top_corner: bool = False, bottom_corner: bool = False) -> None:
        super().__init__('left', fixed=fixed, top_corner=top_corner, bottom_corner=bottom_corner)


class RightDrawer(Drawer):

    def __init__(self, fixed: bool = True, top_corner: bool = False, bottom_corner: bool = False) -> None:
        super().__init__('right', fixed=fixed, top_corner=top_corner, bottom_corner=bottom_corner)


class Footer(Group):

    def __init__(self, fixed: bool = True) -> None:
        view = jp.QFooter(classes='q-pa-md row items-start gap-4', temp=False)
        super().__init__(view)
        code = list(find_parent_page().layout.view)
        code[1] = 'F' if fixed else 'f'
        find_parent_page().layout.view = ''.join(code)


class PageSticky(Group):

    def __init__(self) -> None:
        view = jp.QPageSticky(temp=False)
        super().__init__(view)
