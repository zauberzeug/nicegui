from __future__ import annotations
import asyncio
from typing import Callable
import uuid
from justpy.htmlcomponents import WebPage
import numpy as np
from .element import Element
from .custom_view import CustomView

class ThreeView(CustomView):

    objects: list[Object3D] = []

    def __init__(self, *, width: int, height: int, on_click: Callable):
        dependencies = ['three.min.js', 'OrbitControls.js']
        super().__init__('three', __file__, dependencies, width=width, height=height)
        self.on_click = on_click
        self.allowed_events = ['onConnect', 'onClick']
        self.initialize(temp=False, onConnect=self.handle_connect, onClick=self.handle_click)

    def run_command(self, command: str, socket=None):
        sockets = [socket] if socket is not None else WebPage.sockets.get(Element.wp.page_id, {}).values()
        for socket in sockets:
            asyncio.get_event_loop().create_task(self.run_method(command, socket))

    def handle_connect(self, msg):
        for object in self.objects:
            self.run_command(object._create_command, msg.websocket)
            self.run_command(object._material_command, msg.websocket)
            self.run_command(object._move_command, msg.websocket)
            self.run_command(object._rotate_command, msg.websocket)

    def handle_click(self, msg):
        if self.on_click is not None:
            return self.on_click(msg)
        return False


class Three(Element):

    view: ThreeView = None

    def __init__(self, width: int = 400, height: int = 300, on_click: Callable = None):
        super().__init__(ThreeView(width=width, height=height, on_click=on_click))

    def __enter__(self):
        Three.view = self.view
        return self

    def __exit__(self, *_):
        Three.view = None

class Object3D:

    group_stack: list[Object3D] = []

    def __init__(self, type: str, *args):
        self.view = Three.view
        self.type = type
        self.id = 'scene' if type == 'scene' else str(uuid.uuid4())
        self.parent = Object3D.group_stack[-1] if Object3D.group_stack else None
        self.args = args
        self.color = '#ffffff'
        self.opacity = 1.0
        self.x = 0
        self.y = 0
        self.z = 0
        self.R = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.view.run_command(self._create_command)
        self.view.objects.append(self)

    def __enter__(self):
        Object3D.group_stack.append(self)
        return self

    def __exit__(self, *_):
        Object3D.group_stack.pop()

    @property
    def _create_command(self):
        parent_id = f'"{self.parent.id}"' if self.parent else 'null'
        return f'create("{self.type}", "{self.id}", {parent_id}, {str(self.args)[1:-1]})'

    @property
    def _material_command(self):
        return f'material("{self.id}", "{self.color}", "{self.opacity}")'

    @property
    def _move_command(self):
        return f'move("{self.id}", {self.x}, {self.y}, {self.z})'

    @property
    def _rotate_command(self):
        return f'rotate("{self.id}", {self.R})'

    @property
    def _delete_command(self):
        return f'delete("{self.id}")'

    def material(self, color: str = '#ffffff', opacity: float = 1.0):
        self.color = color
        self.opacity = opacity
        self.view.run_command(self._material_command)
        return self

    def move(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Object3D:
        self.x = x
        self.y = y
        self.z = z
        self.view.run_command(self._move_command)
        return self

    def rotate(self, omega: float, phi: float, kappa: float):
        Rx = np.array([[1, 0, 0], [0, np.cos(omega), -np.sin(omega)], [0, np.sin(omega), np.cos(omega)]])
        Ry = np.array([[np.cos(phi), 0, np.sin(phi)], [0, 1, 0], [-np.sin(phi), 0, np.cos(phi)]])
        Rz = np.array([[np.cos(kappa), -np.sin(kappa), 0], [np.sin(kappa), np.cos(kappa), 0], [0, 0, 1]])
        self.R = (Rz @ Ry @ Rx).tolist()
        self.view.run_command(self._rotate_command)
        return self

    def delete(self):
        self.view.objects = [obj for obj in self.view.objects if obj != self]
        self.view.run_command(self._delete_command)

class Scene(Object3D):

    def __init__(self):
        super().__init__('scene')

class Group(Object3D):

    def __init__(self):
        super().__init__('group')

class Box(Object3D):

    def __init__(self,
                 width: float = 1.0,
                 height: float = 1.0,
                 depth: float = 1.0,
                 ):
        super().__init__('box', width, height, depth)

class Sphere(Object3D):

    def __init__(self,
                 radius: float = 1.0,
                 width_segments: int = 32,
                 height_segments: int = 16,
                 ):
        super().__init__('sphere', radius, width_segments, height_segments)

class Cylinder(Object3D):

    def __init__(self,
                 top_radius: float = 1.0,
                 bottom_radius: float = 1.0,
                 height: float = 1.0,
                 radial_segments: int = 8,
                 height_segments: int = 1,
                 ):
        super().__init__('cylinder', top_radius, bottom_radius, height, radial_segments, height_segments)

class Extrusion(Object3D):

    def __init__(self,
                 outline: list[tuple[float, float]],
                 height: float,
                 ):
        super().__init__('extrusion', outline, height)

class Curve(Object3D):

    def __init__(self,
                 start: tuple[float, float, float],
                 control1: tuple[float, float, float],
                 control2: tuple[float, float, float],
                 end: tuple[float, float, float],
                 num_points: int = 20,
                 ):
        super().__init__('curve', start, control1, control2, end, num_points)

class Texture(Object3D):

    def __init__(self,
                 url: str,
                 coordinates: list[list[tuple[float, float, float]]],
                 ):
        super().__init__('texture', url, coordinates)
