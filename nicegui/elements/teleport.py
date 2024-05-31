from nicegui.element import Element


class Teleport(Element, component="teleport.js"):
    def __init__(self, to: str) -> None:
        """Teleport

        An element that allows us to transmit the content from within a component to any location on the page.

        :param to: the css selector of the element to which we want to teleport the content
        """
        super().__init__()
        self._props["to"] = to

    def force_update(self):
        """This method forces the internal content to be retransmitted to the specified location.

        It is usually called after the target container is rebuilt.
        """
        self.run_method("forceUpdate")
