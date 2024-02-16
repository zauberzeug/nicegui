from typing import Literal, Optional

from . import context
from .element import Element
from .elements.mixins.value_element import ValueElement
from .functions.html import add_body_html
from .logging import log

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
    """
    Represents a header element in a page layout.

    This element is based on Quasar's QHeader component.

    Note: The header is automatically placed above other layout elements in the DOM to improve accessibility.
    To change the order, use the `move` method.

    Args:
        value (bool, optional): Whether the header is already opened. Defaults to True.
        fixed (bool, optional): Whether the header should be fixed to the top of the page. Defaults to True.
        bordered (bool, optional): Whether the header should have a border. Defaults to False.
        elevated (bool, optional): Whether the header should have a shadow. Defaults to False.
        wrap (bool, optional): Whether the header should wrap its content. Defaults to True.
        add_scroll_padding (bool, optional): Whether to automatically prevent link targets from being hidden behind the header. Defaults to True.

    Attributes:
        value (bool): Whether the header is opened.
        fixed (bool): Whether the header is fixed to the top of the page.
        bordered (bool): Whether the header has a border.
        elevated (bool): Whether the header has a shadow.
        wrap (bool): Whether the header wraps its content.
        add_scroll_padding (bool): Whether scroll padding is added to prevent link targets from being hidden.

    Methods:
        toggle(): Toggles the header between opened and closed.
        show(): Shows the header.
        hide(): Hides the header.
    """

    def __init__(self, *,
                 value: bool = True,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False,
                 wrap: bool = True,
                 add_scroll_padding: bool = True,
                 ) -> None:
        """
        Initializes a new instance of the Header class.

        Args:
            value (bool, optional): Whether the header is already opened. Defaults to True.
            fixed (bool, optional): Whether the header should be fixed to the top of the page. Defaults to True.
            bordered (bool, optional): Whether the header should have a border. Defaults to False.
            elevated (bool, optional): Whether the header should have a shadow. Defaults to False.
            wrap (bool, optional): Whether the header should wrap its content. Defaults to True.
            add_scroll_padding (bool, optional): Whether to automatically prevent link targets from being hidden behind the header. Defaults to True.
        """
        _check_current_slot(self)
        with context.get_client().layout:
            super().__init__(tag='q-header', value=value, on_value_change=None)
        self._classes.append('nicegui-header')
        self._props['bordered'] = bordered
        self._props['elevated'] = elevated
        if wrap:
            self._classes.append('wrap')
        code = list(self.client.layout._props['view'])
        code[1] = 'H' if fixed else 'h'
        self.client.layout._props['view'] = ''.join(code)

        self.move(target_index=0)

        if add_scroll_padding:
            add_body_html(f'''
                <script>
                    window.onload = () => {{
                        const header = getElement({self.id}).$el;
                        new ResizeObserver(() => {{
                            document.documentElement.style.scrollPaddingTop = `${{header.offsetHeight}}px`;
                        }}).observe(header);
                    }};
                </script>
            ''')

    def toggle(self):
        """
        Toggles the header between opened and closed.
        """
        self.value = not self.value

    def show(self):
        """
        Shows the header.
        """
        self.value = True

    def hide(self):
        """
        Hides the header.
        """
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
        """Drawer
        This element is based on Quasar's [QDrawer](https://quasar.dev/layout/drawer) component.
        Note: Depending on the side, the drawer is automatically placed above or below the main page container in the DOM to improve accessibility.
        To change the order, use the `move` method.
        - side: side of the page where the drawer should be placed (`left` or `right`)
        - value: whether the drawer is already opened (default: `None`, i.e. if layout width is above threshold)
        - fixed: whether the drawer is fixed or scrolls with the content (default: `True`)
        - bordered: whether the drawer should have a border (default: `False`)
        - elevated: whether the drawer should have a shadow (default: `False`)
        - top_corner: whether the drawer expands into the top corner (default: `False`)
        - bottom_corner: whether the drawer expands into the bottom corner (default: `False`)
        """
        _check_current_slot(self)
        with context.get_client().layout:
            super().__init__('q-drawer')
        if value is None:
            self._props['show-if-above'] = True
        else:
            self._props['model-value'] = value
        self._props['side'] = side
        self._props['bordered'] = bordered
        self._props['elevated'] = elevated
        self._classes.append('nicegui-drawer')
        code = list(self.client.layout._props['view'])
        code[0 if side == 'left' else 2] = side[0].lower() if top_corner else 'h'
        code[4 if side == 'left' else 6] = side[0].upper() if fixed else side[0].lower()
        code[8 if side == 'left' else 10] = side[0].lower() if bottom_corner else 'f'
        self.client.layout._props['view'] = ''.join(code)

        page_container_index = self.client.layout.default_slot.children.index(self.client.page_container)
        self.move(target_index=page_container_index if side == 'left' else page_container_index + 1)

    def toggle(self) -> None:
            """
            Toggle the drawer.

            This method is used to toggle the state of the drawer. When called, it will
            either open or close the drawer, depending on its current state.

            Usage:
                To toggle the drawer, simply call the `toggle` method on an instance of
                the `Drawer` class.

            Returns:
                None
            """
            self.run_method('toggle')
  
    def show(self) -> None:
            """
            Show the drawer.

            This method is used to display the drawer. It executes the 'show' method internally.

            Returns:
                None
            """
            self.run_method('show')

    def hide(self) -> None:
            """
            Hide the drawer.

            This method hides the drawer component. It internally calls the 'hide' method
            to perform the hiding operation.

            Usage:
                drawer.hide()

            Returns:
                None
            """
            self.run_method('hide')


class LeftDrawer(Drawer):
    """
    Left Drawer

    This element is based on Quasar's QDrawer component (https://quasar.dev/layout/drawer).

    Note: The left drawer is automatically placed above the main page container in the DOM to improve accessibility.
    To change the order, use the `move` method.

    - value: Whether the drawer is already opened (default: `None`, i.e. if layout width is above threshold).
    :type value: Optional[bool]
    - fixed: Whether the drawer is fixed or scrolls with the content (default: `True`).
    :type fixed: bool
    - bordered: Whether the drawer should have a border (default: `False`).
    :type bordered: bool
    - elevated: Whether the drawer should have a shadow (default: `False`).
    :type elevated: bool
    - top_corner: Whether the drawer expands into the top corner (default: `False`).
    :type top_corner: bool
    - bottom_corner: Whether the drawer expands into the bottom corner (default: `False`).
    :type bottom_corner: bool
    """

    def __init__(self, *,
                 value: Optional[bool] = None,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False,
                 top_corner: bool = False,
                 bottom_corner: bool = False) -> None:
        """
        Initializes a new instance of the LeftDrawer class.

        - value: Whether the drawer is already opened (default: `None`, i.e. if layout width is above threshold).
        :type value: Optional[bool]
        - fixed: Whether the drawer is fixed or scrolls with the content (default: `True`).
        :type fixed: bool
        - bordered: Whether the drawer should have a border (default: `False`).
        :type bordered: bool
        - elevated: Whether the drawer should have a shadow (default: `False`).
        :type elevated: bool
        - top_corner: Whether the drawer expands into the top corner (default: `False`).
        :type top_corner: bool
        - bottom_corner: Whether the drawer expands into the bottom corner (default: `False`).
        :type bottom_corner: bool
        """
        super().__init__('left',
                         value=value,
                         fixed=fixed,
                         bordered=bordered,
                         elevated=elevated,
                         top_corner=top_corner,
                         bottom_corner=bottom_corner)


class RightDrawer(Drawer):
    """
    A class representing a right drawer element.

    This element is based on Quasar's QDrawer component.
    The right drawer is automatically placed below the main page container in the DOM to improve accessibility.
    To change the order, use the move method.

    Attributes:
        value (Optional[bool]): Whether the drawer is already opened (default: None, i.e. if layout width is above threshold).
        fixed (bool): Whether the drawer is fixed or scrolls with the content (default: True).
        bordered (bool): Whether the drawer should have a border (default: False).
        elevated (bool): Whether the drawer should have a shadow (default: False).
        top_corner (bool): Whether the drawer expands into the top corner (default: False).
        bottom_corner (bool): Whether the drawer expands into the bottom corner (default: False).

    """

    def __init__(self, *,
                 value: Optional[bool] = None,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False,
                 top_corner: bool = False,
                 bottom_corner: bool = False) -> None:
        """
        Initializes a new instance of the RightDrawer class.

        Args:
            value (Optional[bool]): Whether the drawer is already opened (default: None, i.e. if layout width is above threshold).
            fixed (bool): Whether the drawer is fixed or scrolls with the content (default: True).
            bordered (bool): Whether the drawer should have a border (default: False).
            elevated (bool): Whether the drawer should have a shadow (default: False).
            top_corner (bool): Whether the drawer expands into the top corner (default: False).
            bottom_corner (bool): Whether the drawer expands into the bottom corner (default: False).

        Returns:
            None
        """
        super().__init__('right',
                         value=value,
                         fixed=fixed,
                         bordered=bordered,
                         elevated=elevated,
                         top_corner=top_corner,
                         bottom_corner=bottom_corner)


class Footer(ValueElement):
    """
    Footer

    This element is based on Quasar's QFooter component.

    Note: The footer is automatically placed below other layout elements in the DOM to improve accessibility.
    To change the order, use the `move` method.

    Args:
        value (bool, optional): Whether the footer is already opened. Defaults to True.
        fixed (bool, optional): Whether the footer is fixed or scrolls with the content. Defaults to True.
        bordered (bool, optional): Whether the footer should have a border. Defaults to False.
        elevated (bool, optional): Whether the footer should have a shadow. Defaults to False.
        wrap (bool, optional): Whether the footer should wrap its content. Defaults to True.

    Attributes:
        value (bool): Whether the footer is opened or closed.
        fixed (bool): Whether the footer is fixed or scrolls with the content.
        bordered (bool): Whether the footer has a border.
        elevated (bool): Whether the footer has a shadow.
        wrap (bool): Whether the footer wraps its content.

    Methods:
        toggle(): Toggles the footer between opened and closed.
        show(): Shows the footer.
        hide(): Hides the footer.
    """

    def __init__(self, *, value: bool = True, fixed: bool = True, bordered: bool = False, elevated: bool = False, wrap: bool = True) -> None:
        """Footer
        This element is based on Quasar's `QFooter <https://quasar.dev/layout/header-and-footer#qfooter-api>`_ component.
        Note: The footer is automatically placed below other layout elements in the DOM to improve accessibility.
        
        To change the order, use the `move` method.
        
        - value: whether the footer is already opened (default: `True`)
        - fixed: whether the footer is fixed or scrolls with the content (default: `True`)
        - bordered: whether the footer should have a border (default: `False`)
        - elevated: whether the footer should have a shadow (default: `False`)
        - wrap: whether the footer should wrap its content (default: `True`)
        """
        _check_current_slot(self)
        with context.get_client().layout:
            super().__init__(tag='q-footer', value=value, on_value_change=None)
        self.classes('nicegui-footer')
        self._props['bordered'] = bordered
        self._props['elevated'] = elevated
        if wrap:
            self._classes.append('wrap')
        code = list(self.client.layout._props['view'])
        code[9] = 'F' if fixed else 'f'
        self.client.layout._props['view'] = ''.join(code)

        self.move(target_index=-1)

    def toggle(self) -> None:
        """
        Toggles the footer between opened and closed.

        This method changes the value of the footer to its opposite state. If the footer is currently opened, it will be closed after calling this method, and vice versa.

        Usage:
            page_layout = PageLayout()
            page_layout.toggle()

        Returns:
            None
        """
        self.value = not self.value

    def show(self) -> None:
        """
        Shows the footer.

        This method sets the value of the footer to True, indicating that it should be displayed.
        The footer is a component of the page layout and typically contains information such as
        copyright notices, navigation links, or other relevant content.

        Usage:
        To display the footer, simply call the `show` method on the page layout object.

        Example:
        >>> f = Footer()
        >>> f.show()

        Note:
        By default, the footer is hidden. To hide the footer again, you can call the `hide` method.

        """
        self.value = True

    def hide(self) -> None:
        """
        Hides the footer.

        This method sets the value of the footer to False, effectively hiding it from the user interface.

        Usage:
            To hide the footer, simply call the `hide` method on the Footer object.

        Example:
            f = Footer()
            f.hide()
        """
        self.value = False


class PageSticky(Element):
    """A sticky element that is always visible at the bottom of the page.

    This class represents a sticky element that remains fixed at the bottom of the page
    regardless of scrolling. It is designed to be used within a `NiceGUI` application.

    Attributes:
        position (PageStickyPositions): The position of the sticky element. Valid values are:
            - 'bottom-right' (default): Aligns the sticky element to the bottom-right corner of the page.
            - 'bottom-left': Aligns the sticky element to the bottom-left corner of the page.
            - 'top-right': Aligns the sticky element to the top-right corner of the page.
            - 'top-left': Aligns the sticky element to the top-left corner of the page.
        x_offset (float): The horizontal offset of the sticky element from its aligned position.
            Positive values move the element to the right, while negative values move it to the left.
            Default is 0.
        y_offset (float): The vertical offset of the sticky element from its aligned position.
            Positive values move the element downwards, while negative values move it upwards.
            Default is 0.
    """

    def __init__(self, position: PageStickyPositions = 'bottom-right', x_offset: float = 0, y_offset: float = 0) -> None:
        """Page Sticky

        Args:
            - position (PageStickyPositions, optional): The position of the sticky element.
                Defaults to 'bottom-right'.
            - x_offset (float, optional): The horizontal offset of the sticky element.
                Defaults to 0.
            - y_offset (float, optional): The vertical offset of the sticky element.
                Defaults to 0.
        """
        super().__init__('q-page-sticky')
        self._props['position'] = position
        self._props['offset'] = [x_offset, y_offset]


def _check_current_slot(element: Element) -> None:
    """
    Check if the current slot is a top level layout element.

    This function checks if the given element is a top level layout element by comparing its parent with the page content.
    If the parent is not the page content, a warning message is logged indicating that top level layout elements should not be nested.
    This behavior is deprecated and will raise an exception in NiceGUI 1.5.

    Args:
        - element (Element): The element to check.

    Returns:
        None
    """
    parent = context.get_slot().parent
    if parent != parent.client.content:
        log.warning(f'Found top level layout element "{element.__class__.__name__}" inside element "{parent.__class__.__name__}". '
                    'Top level layout elements should not be nested but must be direct children of the page content. '
                    'This will be raising an exception in NiceGUI 1.5')  # DEPRECATED
