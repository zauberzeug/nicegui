
from nicegui import Client, app, context, core, ui
from nicegui.elements.mixins.content_element import ContentElement


class SimulatedScreen:

    def __init__(self) -> None:
        pass

    def open(self, path: str) -> None:
        routes = dict((v, k) for k, v in Client.page_routes.items())
        routes[path]()

    def _find(self, element: ui.element, string: str) -> bool:
        text = element._text or ''
        label = element._props.get('label') or ''
        content = element.content if isinstance(element, ContentElement) else ''
        return (
            any(string in t for t in [text, label, content]) or
            any(self._find(child, string) for child in element)
        )

    def should_contain(self, string: str) -> None:
        assert self._find(context.get_client().page_container, string)

    def click(self, element: ui.element) -> None:
        for listener in element._event_listeners.values():
            if listener.type == 'click' and listener.element_id == element.id:
                element._handle_event({'listener_id': listener.id, 'args': {}})
