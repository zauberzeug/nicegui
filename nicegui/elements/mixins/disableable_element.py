from ...element import Element


class DisableableElement(Element):

    def enable(self) -> None:
        """Enable the element."""
        self.props(remove='disable')

    def disable(self) -> None:
        """Disable the element."""
        self.props(add='disable')

    @property
    def enabled(self) -> bool:
        """Check if the element is enabled."""
        return 'disable' not in self._props
