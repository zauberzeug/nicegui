from typing import Callable
from .element import Element
from .custom_view import CustomView
from .scene_stack import object_stack

class SceneView(CustomView):

    def __init__(self, *, width: int, height: int, on_click: Callable):
        dependencies = ['three.min.js', 'OrbitControls.js']
        super().__init__('scene', __file__, dependencies, width=width, height=height)
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

class Scene(Element):

    from .scene_objects import Group as group
    from .scene_objects import Box as box
    from .scene_objects import Sphere as sphere
    from .scene_objects import Cylinder as cylinder
    from .scene_objects import Extrusion as extrusion
    from .scene_objects import Line as line
    from .scene_objects import Curve as curve
    from .scene_objects import Texture as texture

    def __init__(self, width: int = 400, height: int = 300, on_click: Callable = None):
        super().__init__(SceneView(width=width, height=height, on_click=on_click))

    def __enter__(self):
        self.view_stack.append(self.view)
        scene = self.view.objects[0] if self.view.objects else SceneObject(self.view)
        object_stack.clear()
        object_stack.append(scene)
        return self

    def __exit__(self, *_):
        self.view_stack.pop()

class SceneObject:

    def __init__(self, view: SceneView):
        self.id = 'scene'
        self.view = view
