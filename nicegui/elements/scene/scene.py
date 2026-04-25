import asyncio
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

from typing_extensions import Self

from ... import binding
from ...defaults import DEFAULT_PROP, resolve_defaults
from ...element import Element
from ...events import (
    GenericEventArguments,
    Handler,
    SceneClickEventArguments,
    SceneClickHit,
    SceneDragEventArguments,
    SceneIntersectionPlane,
    ScenePoint,
    handle_event,
)
from .scene_object3d import Object3D


@dataclass(kw_only=True, slots=True)
class SceneCamera:
    type: Literal['perspective', 'orthographic']
    params: dict[str, float]
    x: float = 0
    y: float = -3
    z: float = 5
    look_at_x: float = 0
    look_at_y: float = 0
    look_at_z: float = 0
    up_x: float = 0
    up_y: float = 0
    up_z: float = 1


@dataclass(kw_only=True, slots=True)
class SceneObject:
    id: str = 'scene'


class Scene(Element, component='scene.js', esm={'nicegui-scene': 'dist'}, default_classes='nicegui-scene'):
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

    @resolve_defaults
    def __init__(self,
                 width: int = DEFAULT_PROP | 400,
                 height: int = DEFAULT_PROP | 300,
                 # DEPRECATED: enforce keyword-only arguments in NiceGUI 4.0
                 grid: bool | tuple[int, int] = DEFAULT_PROP | True,
                 camera: SceneCamera | None = None,
                 on_click: Handler[SceneClickEventArguments] | None = None,
                 click_events: list[str] = DEFAULT_PROP | ['click', 'dblclick'],
                 on_drag_start: Handler[SceneDragEventArguments] | None = None,
                 on_drag_end: Handler[SceneDragEventArguments] | None = None,
                 drag_constraints: str = DEFAULT_PROP | '',
                 background_color: str = DEFAULT_PROP | '#eee',
                 control_type: Literal['orbit', 'trackball', 'map'] = DEFAULT_PROP | 'orbit',
                 fps: int = DEFAULT_PROP | 20,
                 show_stats: bool = DEFAULT_PROP | False,
                 intersection_planes: list[SceneIntersectionPlane] | None = None,
                 raycaster_threshold: float = DEFAULT_PROP | 1.0,
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
        :param control_type: type of controls to use for navigating the scene, one of "orbit", "trackball", "map" (default: "orbit", *added in version 3.9.0*)
        :param fps: target frame rate for the scene in frames per second (default: 20, *added in version 3.2.0*)
        :param show_stats: whether to show performance stats (default: ``False``, *added in version 3.2.0*)
        :param intersection_planes: list of named planes to intersect each click ray with.
            The intersection points are surfaced on click events as ``e.intersections[name]``,
            so the host application can read where the ray hit each configured plane even when
            the click lands on empty space. Default: no planes (``e.intersections`` is empty).
        :param raycaster_threshold: hit-test distance threshold (in scene units) for thin objects
            like lines and point clouds. The default value (1.0) matches three.js, which is too
            coarse for scenes with many thin objects (raycasts can return thousands of hits and
            blow past the WebSocket payload limit); lower the threshold for dense scenes.
        """
        super().__init__()
        self._props['width'] = width
        self._props['height'] = height
        self._props['fps'] = fps
        self._props['show-stats'] = show_stats
        self._props['grid'] = grid
        self._props['background-color'] = background_color
        self._props['raycaster-threshold'] = raycaster_threshold
        self._props['intersection-planes'] = [
            {'name': p.name, 'axis': p.axis, 'offset': p.offset}
            for p in (intersection_planes or [])
        ]
        self.camera = camera or self.perspective_camera()
        self._props['camera-type'] = self.camera.type
        self._props['camera-params'] = self.camera.params
        self.objects: dict[str, Object3D] = {}
        self.stack: list[Object3D | SceneObject] = [SceneObject()]
        self._initialized_event = asyncio.Event()
        self._click_handlers = [on_click] if on_click else []
        self._props['click-events'] = click_events[:]
        self._drag_start_handlers = [on_drag_start] if on_drag_start else []
        self._drag_end_handlers = [on_drag_end] if on_drag_end else []
        self.on('init', self._handle_init)
        self.on('click3d', self._handle_click)
        self.on('dragstart', self._handle_drag)
        self.on('dragend', self._handle_drag)
        self._props['drag-constraints'] = drag_constraints
        self._props['control-type'] = control_type

        self._props.add_rename('background_color', 'background-color')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('camera_params', 'camera-params')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('camera_type', 'camera-type')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('click_events', 'click-events')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('drag_constraints', 'drag-constraints')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('show_stats', 'show-stats')  # DEPRECATED: remove in NiceGUI 4.0

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

    def set_axes_inset(self,
                       *,
                       enabled: bool = True,
                       size: int = 128,
                       margin: int = 0,
                       margin_x: int | None = None,
                       margin_y: int | None = None,
                       anchor: Literal['bottom-left', 'bottom-right', 'top-left', 'top-right'] = 'bottom-right',
                       ) -> Self:
        """Toggle and position the orientation axes inset overlay (a small XYZ gizmo).

        Clicking an X/Y/Z axis on the inset snap-animates the camera to look down that axis
        (forwarded to ``viewHelper.handleClick``).

        :param enabled: whether to show the inset (default: ``True``)
        :param size: size of the inset in CSS pixels (default: ``128``)
        :param margin: shorthand for ``margin_x`` and ``margin_y`` (default: ``0``)
        :param margin_x: horizontal margin in pixels from the anchored edge (defaults to ``margin``)
        :param margin_y: vertical margin in pixels from the anchored edge (defaults to ``margin``)
        :param anchor: which corner to pin the inset to (default: ``'bottom-right'``)
        """
        self.run_method('set_axes_inset', {
            'enabled': enabled,
            'size': size,
            'marginX': margin_x if margin_x is not None else margin,
            'marginY': margin_y if margin_y is not None else margin,
            'anchor': anchor,
        })
        return self

    def set_axes_labels(self,
                        *,
                        enabled: bool = True,
                        labels: tuple[str, str, str] = ('X', 'Y', 'Z'),
                        font: str = '24px Arial',
                        color: str = '#000000',
                        radius: float = 14,
                        ) -> Self:
        """Toggle and customize the labels on the orientation axes inset.

        :param enabled: whether to show labels on the inset (default: ``True``)
        :param labels: three label strings for the X, Y, and Z axes (default: ``('X', 'Y', 'Z')``)
        :param font: CSS font shorthand for the label text (default: ``'24px Arial'``)
        :param color: CSS color for the label text (default: ``'#000000'``)
        :param radius: radius of the colored disc behind each label, in canvas pixels (default: ``14``)
        """
        self.run_method('set_axes_labels', {
            'enabled': enabled,
            'labels': list(labels),
            'font': font,
            'color': color,
            'radius': radius,
        })
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

    def _handle_init(self) -> None:
        self._initialized_event.set()
        self.move_camera(duration=0)
        self.run_method('init_objects', [obj.data for obj in self.objects.values()])

    async def initialized(self) -> None:
        """Wait until the scene is initialized."""
        await self.client.connected()
        await self._initialized_event.wait()

    def _handle_click(self, e: GenericEventArguments) -> None:
        # Each configured intersection plane appears in the dict whether the ray hit it or not;
        # the value is `None` for misses so callers can distinguish "plane not configured" from
        # "plane didn't intersect" without `.get()` ambiguity.
        intersections: dict[str, ScenePoint | None] = {
            name: ScenePoint(x=pt['x'], y=pt['y'], z=pt['z']) if pt is not None else None
            for name, pt in e.args['intersections'].items()
        }
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
            intersections=intersections,
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
                    x: float | None = None,
                    y: float | None = None,
                    z: float | None = None,
                    look_at_x: float | None = None,
                    look_at_y: float | None = None,
                    look_at_z: float | None = None,
                    up_x: float | None = None,
                    up_y: float | None = None,
                    up_z: float | None = None,
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

    async def get_camera(self) -> dict[str, Any]:
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
            if predicate(obj) and obj.id in self.objects:  # NOTE: object might have been deleted already by its parent
                obj.delete()

    def clear(self) -> Self:
        """Remove all objects from the scene."""
        super().clear()
        self.delete_objects()
        return self
