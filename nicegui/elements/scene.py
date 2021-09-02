from typing import Callable
from .element import Element
from .custom_view import CustomView
from .scene_object3d import Object3D

class SceneView(CustomView):

    def __init__(self, *, width: int, height: int, on_click: Callable):
        dependencies = ['three.min.js', 'OrbitControls.js']
        super().__init__('scene', __file__, dependencies, width=width, height=height)
        self.on_click = on_click
        self.allowed_events = ['onConnect', 'onClick']
        self.initialize(temp=False, onConnect=self.handle_connect, onClick=self.handle_click)
        self.objects = {}

    def handle_connect(self, msg):
        for object in self.objects.values():
            object.send_to(msg.websocket)

    def handle_click(self, msg):
        for hit in msg.hits:
            hit.object = self.objects.get(hit.object_id)
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
        """3D Scene

        Display a 3d scene using `three.js <https://threejs.org/>`_.
        Currently NiceGUI supports boxes, spheres, cylinders/cones, extrusions, straight lines, curves and textured meshes.
        Objects can be translated, rotated and displayed with different color, opacity or as wireframes.
        They can also be grouped to apply joint movements.

        :param width: width of the canvas
        :param height: height of the canvas
        :param on_click: callback to execute when a 3d object is clicked
        """
        super().__init__(SceneView(width=width, height=height, on_click=on_click))

    def __enter__(self):
        self.view_stack.append(self.view)
        scene = self.view.objects.get('scene', SceneObject(self.view))
        Object3D.stack.clear()
        Object3D.stack.append(scene)
        return self

    def __exit__(self, *_):
        self.view_stack.pop()

class SceneObject:

    def __init__(self, view: SceneView):
        self.id = 'scene'
        self.view = view
