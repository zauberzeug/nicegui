from __future__ import annotations

from typing import Callable, Dict, List, Optional

from ..events import MouseEventArguments, handle_event
from ..vue import register_component
from .mixins.content_element import ContentElement
from .mixins.source_element import SourceElement

register_component('interactive_image', __file__, 'interactive_image.js')


class InteractiveImage(SourceElement, ContentElement):

    def __init__(self, source: str = '', *,
                 on_mouse: Optional[Callable] = None, events: List[str] = ['click'], cross: bool = False) -> None:
        """Interactive Image

        Create an image with an SVG overlay that handles mouse events and yields image coordinates.

        :param source: the source of the image; can be an URL or a base64 string
        :param on_mouse: callback for mouse events (yields `type`, `image_x` and `image_y`)
        :param events: list of JavaScript events to subscribe to (default: `['click']`)
        :param cross: whether to show crosshairs (default: `False`)
        """
        super().__init__(tag='interactive_image', source=source, content='')
        self._props['events'] = events
        self._props['cross'] = cross

        def handle_connect(_) -> None:
            self.run_method('set_source', self.source)
            self.run_method('set_content', self.content)
        self.on('connect', handle_connect)

        def handle_mouse(msg: Dict) -> None:
            if on_mouse is None:
                return
            arguments = MouseEventArguments(
                sender=self,
                client=self.client,
                type=msg['args'].get('mouse_event_type'),
                image_x=msg['args'].get('image_x'),
                image_y=msg['args'].get('image_y'),
            )
            return handle_event(on_mouse, arguments)
        self.on('mouse', handle_mouse)

    def on_source_change(self, source: str) -> None:
        self.run_method('set_source', source)

    def on_content_change(self, content: str) -> None:
        self.run_method('set_content', content)
