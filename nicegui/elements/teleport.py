from ..element import Element


class Teleport(Element, component='teleport.js'):

    def __init__(self, to: str | Element) -> None:
        """Teleport

        An element that allows us to transmit the content from within a component to any location on the page.

        :param to: NiceGUI element or CSS selector of the target element for the teleported content
        """
        super().__init__()
        if isinstance(to, Element):
            to = f'#{to.html_id}'
        self._props['to'] = to
        self._update_method = 'update'
