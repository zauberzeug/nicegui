from typing import Union

from ..element import Element


class Teleport(Element, component='teleport.js'):

    def __init__(self, to: Union[str, Element]) -> None:
        """Teleport

        An element that allows us to transmit the content from within a component to any location on the page.

        :param to: NiceGUI element or CSS selector of the target element for the teleported content
        """
        super().__init__()
        if isinstance(to, Element):
            to = f'#c{to.id}'
        self._props['to'] = to

    def update(self) -> None:
        """Force the internal content to be retransmitted to the specified location.

        This method is usually called after the target container is rebuilt.
        """
        super().update()
        self.run_method('update')
