from ..element import Element


class ContextMenu(Element):

    def __init__(self, *, auto_close: bool = False) -> None:
        """Context Menu

        Creates a context menu based on Quasar's `QMenu <https://quasar.dev/vue-components/menu>`_ component.
        The context menu should be placed inside the element where it should be shown.
        It is automatically opened when the user right-clicks on the element and appears at the mouse position.

        :param auto_close: whether the context menu should be closed after a click on one of its items (default: `False`)
        """
        super().__init__('q-menu')
        self._props['context-menu'] = True
        self._props['touch-position'] = True
        if auto_close:
            self._props['auto-close'] = True

    def open(self) -> None:
        """Open the context menu."""
        self.run_method('show')

    def close(self) -> None:
        """Close the context menu."""
        self.run_method('hide')
