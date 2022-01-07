from typing import Awaitable, Callable, Optional, Union
import traceback
import websockets
from .element import Element
from .custom_view import CustomView
from .page import Page
from .scene_object3d import Object3D
from ..globals import view_stack
from ..events import handle_event

class SceneView(CustomView):

    def __init__(self, *, width: int, height: int, on_click: Union[Callable, Awaitable]):
        dependencies = ['three.min.js', 'OrbitControls.js', 'STLLoader.js']
        super().__init__('scene', __file__, dependencies, width=width, height=height)
        self.on_click = on_click
        self.allowed_events = ['onConnect', 'onClick']
        self.initialize(temp=False, onConnect=self.handle_connect, onClick=self.handle_click)
        self.objects = {}

    def handle_connect(self, msg):
        try:
            for object in self.objects.values():
                object.send_to(msg.websocket)
        except:
            traceback.print_exc()

    def handle_click(self, msg):
        try:
            for hit in msg.hits:
                hit.object = self.objects.get(hit.object_id)
            handle_event(self.on_click, msg, update=self)
            return False
        except:
            traceback.print_exc()

    async def run_method(self, command, websocket):
        try:
            await websocket.send_json({'type': 'run_method', 'data': command, 'id': self.id})
        except (websockets.exceptions.ConnectionClosedOK, RuntimeError):
            pass
        return True

class Scene(Element):
    from .scene_objects import Group as group
    from .scene_objects import Box as box
    from .scene_objects import Sphere as sphere
    from .scene_objects import Cylinder as cylinder
    from .scene_objects import Extrusion as extrusion
    from .scene_objects import Stl as stl
    from .scene_objects import Line as line
    from .scene_objects import Curve as curve
    from .scene_objects import Texture as texture

    def __init__(self, width: int = 400, height: int = 300, on_click: Optional[Union[Callable, Awaitable]] = None):
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
        view_stack.append(self.view)
        scene = self.view.objects.get('scene', SceneObject(self.view, self.page))
        Object3D.stack.clear()
        Object3D.stack.append(scene)
        return self

    def __exit__(self, *_):
        view_stack.pop()

class SceneObject:

    def __init__(self, view: SceneView, page: Page):
        self.id = 'scene'
        self.view = view
        self.page = page
