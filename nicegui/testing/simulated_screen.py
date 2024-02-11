
from nicegui import Client, app, context, core, ui
from nicegui.elements.mixins.content_element import ContentElement


class SimulatedScreen:

    def __init__(self) -> None:
        pass

    def open(self, path: str) -> None:
        routes = dict((v, k) for k, v in Client.page_routes.items())
        routes[path]()

    def _find(self, element: ui.element, string: str) -> ui.element | None:
        text = element._text or ''
        label = element._props.get('label') or ''
        content = element.content if isinstance(element, ContentElement) else ''
        for t in [text, label, content]:
            if string in t:
                return element
        for child in element:
            found = self._find(child, string)
            if found:
                return found
        return None

    def should_contain(self, string: str) -> None:
        if self._find(context.get_client().page_container, string) is not None:
            return
        for m in context.get_client().outbox.messages:
            if m[1] == 'notify' and string in m[2]['message']:
                return
        raise AssertionError(f'text "{string}" not found on current screen')

    def click(self, target_text: str) -> None:
        element = self._find(context.get_client().page_container, target_text)
        assert element
        for listener in element._event_listeners.values():
            if listener.type == 'click' and listener.element_id == element.id:
                element._handle_event({'listener_id': listener.id, 'args': {}})
