from ..element import Element


class ContextMenu(Element):

    def __init__(self) -> None:
        """Context Menu

        Creates a context menu based on Quasar's `QMenu <https://quasar.dev/vue-components/menu>`_ component.
        The context menu should be placed inside the element where it should be shown.
        It is automatically opened when the user right-clicks on the element and appears at the mouse position.
        """
        super().__init__('q-menu')
        self._props['context-menu'] = True
        self._props['touch-position'] = True

    def open(self) -> None:
        """Open the context menu."""
        self.run_method('show')

    def close(self) -> None:
        """Close the context menu."""
        self.run_method('hide')
