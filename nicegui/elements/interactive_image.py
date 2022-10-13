from __future__ import annotations

import traceback
from typing import Any, Callable, Dict, List, Optional

from justpy import WebPage

from ..binding import BindableProperty, BindSourceMixin
from ..events import MouseEventArguments, handle_event
from ..routes import add_dependencies
from .custom_view import CustomView
from .element import Element

add_dependencies(__file__)


class InteractiveImageView(CustomView):

    def __init__(self, source: str, on_mouse: Callable, events: List[str], cross: bool):
        super().__init__('interactive_image', source=source, events=events, cross=cross, svg_content='')
        self.allowed_events = ['onMouse', 'onConnect']
        self.initialize(onMouse=on_mouse, onConnect=self.on_connect)
        self.sockets = []

    def on_connect(self, msg):
        self.prune_sockets()
        self.sockets.append(msg.websocket)

    def prune_sockets(self):
        page_sockets = [s for page_id in self.pages for s in WebPage.sockets.get(page_id, {}).values()]
        self.sockets = [s for s in self.sockets if s in page_sockets]


def _handle_source_change(sender: Element, source: str) -> None:
    sender.view.options.source = source
    sender.update()


class InteractiveImage(Element, BindSourceMixin):
    source = BindableProperty(on_change=_handle_source_change)

    def __init__(self, source: str = '', *,
                 on_mouse: Optional[Callable] = None, events: List[str] = ['click'], cross: bool = False):
        """Interactive Image

        Create an image with an SVG overlay that handles mouse events and yields image coordinates.

        :param source: the source of the image; can be an URL or a base64 string
        :param on_mouse: callback for mouse events (yields `type`, `image_x` and `image_y`)
        :param events: list of JavaScript events to subscribe to (default: `['click']`)
        :param cross: whether to show crosshairs (default: `False`)
        """
        self.mouse_handler = on_mouse
        super().__init__(InteractiveImageView(source, self.handle_mouse, events, cross))

        self.source = source

    def handle_mouse(self, msg: Dict[str, Any]) -> Optional[bool]:
        if self.mouse_handler is None:
            return False
        try:
            arguments = MouseEventArguments(
                sender=self,
                socket=msg.get('websocket'),
                type=msg.get('mouse_event_type'),
                image_x=msg.get('image_x'),
                image_y=msg.get('image_y'),
            )
            return handle_event(self.mouse_handler, arguments)
        except:
            traceback.print_exc()

    async def set_source(self, source: str):
        self.view.options.source = source
        self.view.prune_sockets()
        for socket in self.view.sockets:
            await self.view.run_method(f'set_source("{source}")', socket)

    @property
    def svg_content(self) -> str:
        return self.view.options.svg_content

    @svg_content.setter
    def svg_content(self, content: str):
        self.view.options.svg_content = content
