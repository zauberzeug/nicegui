from nicegui.element import Element


class Teleport(Element, component="teleport.js"):
    def __init__(self, to: str) -> None:
        """Teleport

        An element enables us to transmit the content from within a component to any location on the page.

        :param to: the selector of the element to which we want to teleport the content
        """
        super().__init__()
        self._props["to"] = to

    def force_update(self):
        """Force update.This method can be used to force the update of the content in the teleported element.
        """
        self.run_method("forceUpdate")


