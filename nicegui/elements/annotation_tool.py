from __future__ import annotations
from typing import Callable
import traceback
from ..events import ImageClickEventArguments, handle_event
from .custom_view import CustomView
from .element import Element

CustomView.use(__file__)

class AnnotationToolView(CustomView):

    def __init__(self, source: str, on_click: Callable):
        super().__init__('annotation_tool', source=source)
        self.allowed_events = ['onClick']
        self.initialize(onClick=on_click)

class AnnotationTool(Element):

    def __init__(self, source: str, on_click: Callable):
        """Annotation Tool

        Create a special image that handles mouse clicks and yields image coordinates.

        :param source: the source of the image; can be an url or a base64 string
        :param on_click: callback for when the user clicks on the image (yields `image_x` and `image_y`)
        """
        self.click_handler = on_click
        super().__init__(AnnotationToolView(source, self.handle_click))

    def handle_click(self, msg):
        try:
            arguments = ImageClickEventArguments(
                sender=self,
                socket=msg.get('websocket'),
                image_x=msg.get('image_x'),
                image_y=msg.get('image_y'),
            )
            handle_event(self.click_handler, arguments)
        except:
            traceback.print_exc()
