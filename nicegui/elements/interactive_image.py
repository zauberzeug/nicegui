from __future__ import annotations

from typing import Callable, Dict, List, Optional

from ..dependencies import register_component
from ..events import MouseEventArguments, handle_event
from .mixins.content_element import ContentElement
from .mixins.source_element import SourceElement

register_component('interactive_image', __file__, 'interactive_image.js')


class InteractiveImage(SourceElement, ContentElement):

    def __init__(self, source: str = '', *,
                 content: str = '',
                 on_mouse: Optional[Callable] = None, events: List[str] = ['click'], cross: bool = False) -> None:
        """Interactive Image

        Create an image with an SVG overlay that handles mouse events and yields image coordinates.
        It is also the best choice for non-flickering image updates.
        If the source URL changes faster than images can be loaded by the browser, some images are simply skipped.
        Thereby a stream of images automatically adapts to the available bandwidth.
        See `OpenCV Webcam <https://github.com/zauberzeug/nicegui/tree/main/examples/opencv_webcam/main.py>`_ for an example.

        :param source: the source of the image; can be an URL or a base64 string
        :param content: SVG content which should be overlayed; viewport has the same dimensions as the image
        :param on_mouse: callback for mouse events (yields `type`, `image_x` and `image_y`)
        :param events: list of JavaScript events to subscribe to (default: `['click']`)
        :param cross: whether to show crosshairs (default: `False`)
        """
        super().__init__(tag='interactive_image', source=source, content=content)
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
