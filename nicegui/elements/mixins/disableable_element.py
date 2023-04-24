from ...binding import BindableProperty
from ...element import Element


class DisableableElement(Element):
    enabled = BindableProperty(on_change=lambda sender, value: sender.on_enabled_change(value))

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.enabled = True

    def enable(self) -> None:
        """Enable the element."""
        self.enabled = True

    def disable(self) -> None:
        """Disable the element."""
        self.enabled = False

    def set_enabled(self, value: bool) -> None:
        """Set the enabled state of the element."""
        self.enabled = value

    def on_enabled_change(self, enabled: bool) -> None:
        """Called when the element is enabled or disabled.

        :param enabled: The new state.
        """
        self._props['disable'] = not enabled
        self.update()
