from ..element import Element


class ContextMenu(Element):
    """
    Represents a context menu that can be shown when the user right-clicks on an element.

    The context menu is based on Quasar's QMenu component and is automatically opened at the mouse position.

    Usage:
    1. Create an instance of ContextMenu.
    2. Add menu items using the `add_item` method.
    3. Attach the context menu to an element using the `attach_to_element` method.
    4. The context menu will be automatically opened when the user right-clicks on the attached element.

    Example:
    ```python
    # Create a context menu
    context_menu = ContextMenu()

    # Add menu items
    context_menu.add_item('Copy', lambda: print('Copy clicked'))
    context_menu.add_item('Paste', lambda: print('Paste clicked'))

    # Attach the context menu to an element
    element.attach_context_menu(context_menu)
    ```

    Note:
    - The `add_item` method allows you to add menu items to the context menu.
    - The `attach_to_element` method attaches the context menu to an element.
    - The `open` method opens the context menu.
    - The `close` method closes the context menu.
    """

    def __init__(self) -> None:
        """
        ContextMenu
        
        Represents a context menu that can be shown when the user right-clicks on an element.

        The context menu is based on Quasar's QMenu component and is automatically opened at the mouse position.

        Usage:
        
        1. Create an instance of ContextMenu.
        2. Add menu items using the `add_item` method.
        3. Attach the context menu to an element using the `attach_to_element` method.
        4. The context menu will be automatically opened when the user right-clicks on the attached element.

        Note:
        
        - The `add_item` method allows you to add menu items to the context menu.
        - The `attach_to_element` method attaches the context menu to an element.
        - The `open` method opens the context menu.
        - The `close` method closes the context menu.
        """
        super().__init__('q-menu')
        self._props['context-menu'] = True
        self._props['touch-position'] = True

    def open(self) -> None:
            """
            Opens the context menu.

            This method is used to display the context menu on the screen. It triggers the 'show' method internally,
            which handles the rendering and display of the menu.

            Usage:
                context_menu = ContextMenu()
                context_menu.open()

            Returns:
                None
            """
            self.run_method('show')

    def close(self) -> None:
            """
            Closes the context menu.

            This method hides the context menu, making it invisible to the user.
            It should be called when the context menu is no longer needed or when
            the user wants to dismiss it.

            Usage:
                context_menu.close()

            Returns:
                None
            """
            self.run_method('hide')
