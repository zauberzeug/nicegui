from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union

from .. import binding, globals
from ..element import Element
from ..events import GenericEventArguments, SceneClickEventArguments, SceneClickHit, handle_event
from ..helpers import KWONLY_SLOTS
from .scene_object3d import Object3D


@dataclass(**KWONLY_SLOTS)
class SceneCamera:
    x: float = 0
    y: float = -3
    z: float = 5
    look_at_x: float = 0
    look_at_y: float = 0
    look_at_z: float = 0
    up_x: float = 0
    up_y: float = 0
    up_z: float = 1


@dataclass(**KWONLY_SLOTS)
class SceneObject:
    id: str = 'scene'


class Scene(Element,
            component='scene.js',
            libraries=['lib/tween/tween.umd.js'],
            exposed_libraries=[
                'lib/three/three.module.js',
                'lib/three/modules/CSS2DRenderer.js',
                'lib/three/modules/CSS3DRenderer.js',
                'lib/three/modules/OrbitControls.js',
                'lib/three/modules/STLLoader.js',
            ]):
    from .scene_objects import Box as box
    from .scene_objects import Curve as curve
    from .scene_objects import Cylinder as cylinder
    from .scene_objects import Extrusion as extrusion
    from .scene_objects import Group as group
    from .scene_objects import Line as line
    from .scene_objects import PointCloud as point_cloud
    from .scene_objects import QuadraticBezierTube as quadratic_bezier_tube
    from .scene_objects import Ring as ring
    from .scene_objects import Sphere as sphere
    from .scene_objects import SpotLight as spot_light
    from .scene_objects import Stl as stl
    from .scene_objects import Text as text
    from .scene_objects import Text3d as text3d
    from .scene_objects import Texture as texture

    def __init__(self,
                 width: int = 400,
                 height: int = 300,
                 grid: bool = True,
                 on_click: Optional[Callable[..., Any]] = None,
                 ) -> None:
        """3D Scene

        Display a 3d scene using `three.js <https://threejs.org/>`_.
        Currently NiceGUI supports boxes, spheres, cylinders/cones, extrusions, straight lines, curves and textured meshes.
        Objects can be translated, rotated and displayed with different color, opacity or as wireframes.
        They can also be grouped to apply joint movements.

        :param width: width of the canvas
        :param height: height of the canvas
        :param grid: whether to display a grid
        :param on_click: callback to execute when a 3d object is clicked
        """
        super().__init__()
        self._props['width'] = width
        self._props['height'] = height
        self._props['grid'] = grid
        self.objects: Dict[str, Object3D] = {}
        self.stack: List[Union[Object3D, SceneObject]] = [SceneObject()]
        self.camera: SceneCamera = SceneCamera()
        self.on_click = on_click
        self.is_initialized = False
        self.on('init', self.handle_init)
        self.on('click3d', self.handle_click)

    def handle_init(self, e: GenericEventArguments) -> None:
        self.is_initialized = True
        with globals.socket_id(e.args['socket_id']):
            self.move_camera(duration=0)
            for object in self.objects.values():
                object.send()

    def run_method(self, name: str, *args: Any) -> None:
        if not self.is_initialized:
            return
        super().run_method(name, *args)

    def handle_click(self, e: GenericEventArguments) -> None:
        arguments = SceneClickEventArguments(
            sender=self,
            client=self.client,
            click_type=e.args['click_type'],
            button=e.args['button'],
            alt=e.args['alt_key'],
            ctrl=e.args['ctrl_key'],
            meta=e.args['meta_key'],
            shift=e.args['shift_key'],
            hits=[SceneClickHit(
                object_id=hit['object_id'],
                object_name=hit['object_name'],
                x=hit['point']['x'],
                y=hit['point']['y'],
                z=hit['point']['z'],
            ) for hit in e.args['hits']],
        )
        handle_event(self.on_click, arguments)

    def __len__(self) -> int:
        return len(self.objects)

    def move_camera(self,
                    x: Optional[float] = None,
                    y: Optional[float] = None,
                    z: Optional[float] = None,
                    look_at_x: Optional[float] = None,
                    look_at_y: Optional[float] = None,
                    look_at_z: Optional[float] = None,
                    up_x: Optional[float] = None,
                    up_y: Optional[float] = None,
                    up_z: Optional[float] = None,
                    duration: float = 0.5) -> None:
        self.camera.x = self.camera.x if x is None else x
        self.camera.y = self.camera.y if y is None else y
        self.camera.z = self.camera.z if z is None else z
        self.camera.look_at_x = self.camera.look_at_x if look_at_x is None else look_at_x
        self.camera.look_at_y = self.camera.look_at_y if look_at_y is None else look_at_y
        self.camera.look_at_z = self.camera.look_at_z if look_at_z is None else look_at_z
        self.camera.up_x = self.camera.up_x if up_x is None else up_x
        self.camera.up_y = self.camera.up_y if up_y is None else up_y
        self.camera.up_z = self.camera.up_z if up_z is None else up_z
        self.run_method('move_camera',
                        self.camera.x, self.camera.y, self.camera.z,
                        self.camera.look_at_x, self.camera.look_at_y, self.camera.look_at_z,
                        self.camera.up_x, self.camera.up_y, self.camera.up_z, duration)

    def delete(self) -> None:
        binding.remove(list(self.objects.values()), Object3D)
        super().delete()
