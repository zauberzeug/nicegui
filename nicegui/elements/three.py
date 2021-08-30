from typing import Callable
from .element import Element
from .custom_view import CustomView
from .three_stack import object_stack

class ThreeView(CustomView):

    def __init__(self, *, width: int, height: int, on_click: Callable):
        dependencies = ['three.min.js', 'OrbitControls.js']
        super().__init__('three', __file__, dependencies, width=width, height=height)
        self.on_click = on_click
        self.allowed_events = ['onConnect', 'onClick']
        self.initialize(temp=False, onConnect=self.handle_connect, onClick=self.handle_click)
        self.objects = []

    def handle_connect(self, msg):
        for object in self.objects:
            object.send_to(msg.websocket)

    def handle_click(self, msg):
        if self.on_click is not None:
            return self.on_click(msg)
        return False

class Three(Element):

    from .three_objects import Group as group
    from .three_objects import Box as box
    from .three_objects import Sphere as sphere
    from .three_objects import Cylinder as cylinder
    from .three_objects import Extrusion as extrusion
    from .three_objects import Line as line
    from .three_objects import Curve as curve
    from .three_objects import Texture as texture

    def __init__(self, width: int = 400, height: int = 300, on_click: Callable = None):
        super().__init__(ThreeView(width=width, height=height, on_click=on_click))

    def __enter__(self):
        self.view_stack.append(self.view)
        scene = self.view.objects[0] if self.view.objects else Scene(self.view)
        object_stack.clear()
        object_stack.append(scene)
        return self

    def __exit__(self, *_):
        self.view_stack.pop()

class Scene:

    def __init__(self, view: ThreeView):
        self.id = 'scene'
        self.view = view
