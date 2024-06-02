from nicegui.element import Element


class Teleport(Element, component='teleport.js'):

    def __init__(self, to: str) -> None:
        """Teleport

        An element that allows us to transmit the content from within a component to any location on the page.

        :param to: CSS selector of the target element for the teleported content
        """
        super().__init__()
        self._props['to'] = to

    def force_update(self) -> None:
        """Force the internal content to be retransmitted to the specified location.

        This method is usually called after the target container is rebuilt.
        """
        self.run_method('forceUpdate')
