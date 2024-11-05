import asyncio
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union

from typing_extensions import Self

from .. import binding
from ..dataclasses import KWONLY_SLOTS
from ..element import Element
from ..events import (
    GenericEventArguments,
    Handler,
    SceneClickEventArguments,
    SceneClickHit,
    SceneDragEventArguments,
    handle_event,
)
from .scene_object3d import Object3D


@dataclass(**KWONLY_SLOTS)
class SceneCamera:
    type: Literal['perspective', 'orthographic']
    params: Dict[str, float]
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
            dependencies=[
                'lib/three/three.module.js',
                'lib/three/modules/BufferGeometryUtils.js',
                'lib/three/modules/CSS2DRenderer.js',
                'lib/three/modules/CSS3DRenderer.js',
                'lib/three/modules/DragControls.js',
                'lib/three/modules/GLTFLoader.js',
                'lib/three/modules/OrbitControls.js',
                'lib/three/modules/STLLoader.js',
                'lib/tween/tween.umd.js',
            ],
            default_classes='nicegui-scene'):
    # pylint: disable=import-outside-toplevel
    from .scene_objects import AxesHelper as axes_helper
    from .scene_objects import Box as box
    from .scene_objects import Curve as curve
    from .scene_objects import Cylinder as cylinder
    from .scene_objects import Extrusion as extrusion
    from .scene_objects import Gltf as gltf
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
                 grid: Union[bool, Tuple[int, int]] = True,
                 camera: Optional[SceneCamera] = None,
                 on_click: Optional[Handler[SceneClickEventArguments]] = None,
                 click_events: List[str] = ['click', 'dblclick'],  # noqa: B006
                 on_drag_start: Optional[Handler[SceneDragEventArguments]] = None,
                 on_drag_end: Optional[Handler[SceneDragEventArguments]] = None,
                 drag_constraints: str = '',
                 background_color: str = '#eee',
                 ) -> None:
        """3D Scene

        Display a 3D scene using `three.js <https://threejs.org/>`_.
        Currently NiceGUI supports boxes, spheres, cylinders/cones, extrusions, straight lines, curves and textured meshes.
        Objects can be translated, rotated and displayed with different color, opacity or as wireframes.
        They can also be grouped to apply joint movements.

        :param width: width of the canvas
        :param height: height of the canvas
        :param grid: whether to display a grid (boolean or tuple of ``size`` and ``divisions`` for `Three.js' GridHelper <https://threejs.org/docs/#api/en/helpers/GridHelper>`_, default: 100x100)
        :param camera: camera definition, either instance of ``ui.scene.perspective_camera`` (default) or ``ui.scene.orthographic_camera``
        :param on_click: callback to execute when a 3D object is clicked (use ``click_events`` to specify which events to subscribe to)
        :param click_events: list of JavaScript click events to subscribe to (default: ``['click', 'dblclick']``)
        :param on_drag_start: callback to execute when a 3D object is dragged
        :param on_drag_end: callback to execute when a 3D object is dropped
        :param drag_constraints: comma-separated JavaScript expression for constraining positions of dragged objects (e.g. ``'x = 0, z = y / 2'``)
        :param background_color: background color of the scene (default: "#eee")
        """
        super().__init__()
        self._props['width'] = width
        self._props['height'] = height
        self._props['grid'] = grid
        self._props['background_color'] = background_color
        self.camera = camera or self.perspective_camera()
        self._props['camera_type'] = self.camera.type
        self._props['camera_params'] = self.camera.params
        self.objects: Dict[str, Object3D] = {}
        self.stack: List[Union[Object3D, SceneObject]] = [SceneObject()]
        self._click_handlers = [on_click] if on_click else []
        self._props['click_events'] = click_events
        self._drag_start_handlers = [on_drag_start] if on_drag_start else []
        self._drag_end_handlers = [on_drag_end] if on_drag_end else []
        self.on('init', self._handle_init)
        self.on('click3d', self._handle_click)
        self.on('dragstart', self._handle_drag)
        self.on('dragend', self._handle_drag)
        self._props['drag_constraints'] = drag_constraints

    def on_click(self, callback: Handler[SceneClickEventArguments]) -> Self:
        """Add a callback to be invoked when a 3D object is clicked."""
        self._click_handlers.append(callback)
        return self

    def on_drag_start(self, callback: Handler[SceneDragEventArguments]) -> Self:
        """Add a callback to be invoked when a 3D object is dragged."""
        self._drag_start_handlers.append(callback)
        return self

    def on_drag_end(self, callback: Handler[SceneDragEventArguments]) -> Self:
        """Add a callback to be invoked when a 3D object is dropped."""
        self._drag_end_handlers.append(callback)
        return self

    @staticmethod
    def perspective_camera(*, fov: float = 75, near: float = 0.1, far: float = 1000) -> SceneCamera:
        """Create a perspective camera.

        :param fov: vertical field of view in degrees
        :param near: near clipping plane
        :param far: far clipping plane
        """
        return SceneCamera(type='perspective', params={'fov': fov, 'near': near, 'far': far})

    @staticmethod
    def orthographic_camera(*, size: float = 10, near: float = 0.1, far: float = 1000) -> SceneCamera:
        """Create a orthographic camera.

        The size defines the vertical size of the view volume, i.e. the distance between the top and bottom clipping planes.
        The left and right clipping planes are set such that the aspect ratio matches the viewport.

        :param size: vertical size of the view volume
        :param near: near clipping plane
        :param far: far clipping plane
        """
        return SceneCamera(type='orthographic', params={'size': size, 'near': near, 'far': far})

    def __enter__(self) -> Self:
        Object3D.current_scene = self
        super().__enter__()
        return self

    def __getattribute__(self, name: str) -> Any:
        attribute = super().__getattribute__(name)
        if isinstance(attribute, type) and issubclass(attribute, Object3D):
            Object3D.current_scene = self
        return attribute

    def _handle_init(self, e: GenericEventArguments) -> None:
        with self.client.individual_target(e.args['socket_id']):
            self.move_camera(duration=0)
            self.run_method('init_objects', [obj.data for obj in self.objects.values()])

    async def initialized(self) -> None:
        """Wait until the scene is initialized."""
        event = asyncio.Event()
        self.on('init', event.set, [])
        await self.client.connected()
        await event.wait()

    def _handle_click(self, e: GenericEventArguments) -> None:
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
        for handler in self._click_handlers:
            handle_event(handler, arguments)

    def _handle_drag(self, e: GenericEventArguments) -> None:
        arguments = SceneDragEventArguments(
            sender=self,
            client=self.client,
            type=e.args['type'],
            object_id=e.args['object_id'],
            object_name=e.args['object_name'],
            x=e.args['x'],
            y=e.args['y'],
            z=e.args['z'],
        )
        if arguments.type == 'dragend':
            self.objects[arguments.object_id].move(arguments.x, arguments.y, arguments.z)

        for handler in (self._drag_start_handlers if arguments.type == 'dragstart' else self._drag_end_handlers):
            handle_event(handler, arguments)

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
        """Move the camera to a new position.

        :param x: camera x position
        :param y: camera y position
        :param z: camera z position
        :param look_at_x: camera look-at x position
        :param look_at_y: camera look-at y position
        :param look_at_z: camera look-at z position
        :param up_x: x component of the camera up vector
        :param up_y: y component of the camera up vector
        :param up_z: z component of the camera up vector
        :param duration: duration of the movement in seconds (default: `0.5`)
        """
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

    async def get_camera(self) -> Dict[str, Any]:
        """Get the current camera parameters.

        In contrast to the `camera` property,
        the result of this method includes the current camera pose caused by the user navigating the scene in the browser.
        """
        return await self.run_method('get_camera')

    def _handle_delete(self) -> None:
        binding.remove(list(self.objects.values()))
        super()._handle_delete()

    def delete_objects(self, predicate: Callable[[Object3D], bool] = lambda _: True) -> None:
        """Remove objects from the scene.

        :param predicate: function which returns `True` for objects which should be deleted
        """
        for obj in list(self.objects.values()):
            if predicate(obj):
                obj.delete()

    def clear(self) -> None:
        """Remove all objects from the scene."""
        super().clear()
        self.delete_objects()
