from __future__ import annotations
from typing import Callable
import traceback
from ..events import MouseEventArguments, handle_event
from .custom_view import CustomView
from .element import Element

CustomView.use(__file__)

class AnnotationToolView(CustomView):

    def __init__(self, source: str, on_mouse: Callable, events: list[str]):
        super().__init__('annotation_tool', source=source, events=events)
        self.allowed_events = ['onMouse']
        self.initialize(onMouse=on_mouse)

class AnnotationTool(Element):

    def __init__(self, source: str, on_mouse: Callable, events: list[str] = ['click']):
        """Annotation Tool

        Create a special image that handles mouse clicks and yields image coordinates.

        :param source: the source of the image; can be an url or a base64 string
        :param on_mouse: callback for mouse events (yields `type`, `image_x` and `image_y`)
        :param events: list of JavaScript events to subscribe to
        """
        self.mouse_handler = on_mouse
        super().__init__(AnnotationToolView(source, self.handle_mouse, events))

    def handle_mouse(self, msg):
        try:
            arguments = MouseEventArguments(
                sender=self,
                socket=msg.get('websocket'),
                type=msg.get('mouse_event_type'),
                image_x=msg.get('image_x'),
                image_y=msg.get('image_y'),
            )
            handle_event(self.mouse_handler, arguments)
        except:
            traceback.print_exc()
