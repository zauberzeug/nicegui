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
    SceneClipPlane,
    SceneDragEventArguments,
    SceneGroundPoint,
    SceneTransformEventArguments,
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
    from .scene_objects import ArrowHelper as arrow_helper
    from .scene_objects import AxesHelper as axes_helper
    from .scene_objects import Box as box
    from .scene_objects import Curve as curve
    from .scene_objects import Cylinder as cylinder
    from .scene_objects import Extrusion as extrusion
    from .scene_objects import Gltf as gltf
    from .scene_objects import Group as group
    from .scene_objects import Lathe as lathe
    from .scene_objects import Line as line
    from .scene_objects import PointCloud as point_cloud
    from .scene_objects import PolarGridHelper as polar_grid_helper
    from .scene_objects import Polyline as polyline
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
                 polar_grid: tuple[float, int, int] | None = None,
                 camera: SceneCamera | None = None,
                 on_click: Handler[SceneClickEventArguments] | None = None,
                 click_events: list[str] = DEFAULT_PROP | ['click', 'dblclick'],
                 on_drag_start: Handler[SceneDragEventArguments] | None = None,
                 on_drag_end: Handler[SceneDragEventArguments] | None = None,
                 on_transform: Handler[SceneTransformEventArguments] | None = None,
                 on_transform_start: Handler[SceneTransformEventArguments] | None = None,
                 on_transform_end: Handler[SceneTransformEventArguments] | None = None,
                 drag_constraints: str = DEFAULT_PROP | '',
                 background_color: str = DEFAULT_PROP | '#eee',
                 control_type: Literal['orbit', 'trackball', 'map'] = DEFAULT_PROP | 'orbit',
                 fps: int = DEFAULT_PROP | 20,
                 show_stats: bool = DEFAULT_PROP | False,
                 raycaster_threshold: float = DEFAULT_PROP | 1.0,
                 hover_color: int = DEFAULT_PROP | 0xFFFFFF,
                 hover_opacity: float = DEFAULT_PROP | 0.2,
                 hover_scale: float = DEFAULT_PROP | 1.05,
                 ground_axis: Literal['x', 'y', 'z'] = DEFAULT_PROP | 'z',
                 ground_offset: float = DEFAULT_PROP | 0.0,
                 ) -> None:
        """3D Scene

        Display a 3D scene using `three.js <https://threejs.org/>`_.
        Currently NiceGUI supports boxes, spheres, cylinders/cones, extrusions, straight lines, curves and textured meshes.
        Objects can be translated, rotated and displayed with different color, opacity or as wireframes.
        They can also be grouped to apply joint movements.

        :param width: width of the canvas
        :param height: height of the canvas
        :param grid: whether to display a grid (boolean or tuple of ``size`` and ``divisions`` for `Three.js' GridHelper <https://threejs.org/docs/#api/en/helpers/GridHelper>`_, default: 100x100)
        :param polar_grid: optional tuple of ``(radius, sectors, rings)`` for `Three.js' PolarGridHelper <https://threejs.org/docs/#api/en/helpers/PolarGridHelper>`_ (default: ``None``)
        :param camera: camera definition, either instance of ``ui.scene.perspective_camera`` (default) or ``ui.scene.orthographic_camera``
        :param on_click: callback to execute when a 3D object is clicked (use ``click_events`` to specify which events to subscribe to)
        :param click_events: list of JavaScript click events to subscribe to (default: ``['click', 'dblclick']``)
        :param on_drag_start: callback to execute when a 3D object is dragged
        :param on_drag_end: callback to execute when a 3D object is dropped
        :param on_transform: callback executed continuously while an object is being transformed via TransformControls
        :param on_transform_start: callback executed when TransformControls gizmo interaction starts
        :param on_transform_end: callback executed when TransformControls gizmo interaction ends
        :param drag_constraints: comma-separated JavaScript expression for constraining positions of dragged objects (e.g. ``'x = 0, z = y / 2'``)
        :param background_color: background color of the scene (default: "#eee")
        :param control_type: type of controls to use for navigating the scene, one of "orbit", "trackball", "map" (default: "orbit", *added in version 3.9.0*)
        :param fps: target frame rate for the scene in frames per second (default: 20, *added in version 3.2.0*)
        :param show_stats: whether to show performance stats (default: ``False``, *added in version 3.2.0*)
        :param raycaster_threshold: hit-test threshold for thin objects like ``line`` and point clouds (default: 1.0).
            Lower values reduce the number of hits from dense thin objects, preventing large WebSocket payloads on click events.
        :param hover_color: hex color of the hover glow overlay applied to ``hoverable`` objects (default: ``0xFFFFFF``)
        :param hover_opacity: opacity of the hover glow overlay (default: ``0.2``)
        :param hover_scale: scale multiplier applied to the hover glow relative to the source mesh (default: ``1.05``, i.e. 5% larger than the mesh)
        :param ground_axis: axis normal to the ground plane used for :class:`SceneGroundPoint` ray intersection, one of ``'x'``, ``'y'``, ``'z'`` (default: ``'z'``)
        :param ground_offset: signed offset of the ground plane along ``ground_axis`` (default: ``0.0``)
        """
        super().__init__()
        self._props['width'] = width
        self._props['height'] = height
        self._props['fps'] = fps
        self._props['show-stats'] = show_stats
        self._props['grid'] = grid
        self._props['polar-grid'] = polar_grid
        self._props['background-color'] = background_color
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
        self._transform_handlers: list[Handler[SceneTransformEventArguments]] = \
            [on_transform] if on_transform else []
        self._transform_start_handlers: list[Handler[SceneTransformEventArguments]] = \
            [on_transform_start] if on_transform_start else []
        self._transform_end_handlers: list[Handler[SceneTransformEventArguments]] = \
            [on_transform_end] if on_transform_end else []
        self.on('init', self._handle_init)
        self.on('click3d', self._handle_click)
        self.on('dragstart', self._handle_drag)
        self.on('dragend', self._handle_drag)
        self.on('transform', self._handle_transform)
        self.on('transform_start', self._handle_transform)
        self.on('transform_end', self._handle_transform)
        self._props['drag-constraints'] = drag_constraints
        self._props['control-type'] = control_type
        self._props['raycaster-threshold'] = raycaster_threshold
        self._props['hover-color'] = hover_color
        self._props['hover-opacity'] = hover_opacity
        self._props['hover-scale'] = hover_scale
        self._props['ground-axis'] = ground_axis
        self._props['ground-offset'] = ground_offset

        self._props.add_rename('background_color', 'background-color')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('camera_params', 'camera-params')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('camera_type', 'camera-type')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('click_events', 'click-events')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('drag_constraints', 'drag-constraints')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('polar_grid', 'polar-grid')  # DEPRECATED: remove in NiceGUI 4.0
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

    def on_transform(self, callback: Handler[SceneTransformEventArguments]) -> Self:
        """Add a callback to be invoked continuously while a 3D object is being transformed."""
        self._transform_handlers.append(callback)
        return self

    def on_transform_start(self, callback: Handler[SceneTransformEventArguments]) -> Self:
        """Add a callback to be invoked when transform gizmo interaction starts."""
        self._transform_start_handlers.append(callback)
        return self

    def on_transform_end(self, callback: Handler[SceneTransformEventArguments]) -> Self:
        """Add a callback to be invoked when transform gizmo interaction ends."""
        self._transform_end_handlers.append(callback)
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
        gp = e.args.get('ground_point')
        ground_point = SceneGroundPoint(x=gp['x'], y=gp['y'], z=gp['z']) if gp else None
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
            ground_point=ground_point,
            screen_x=e.args.get('screen_x'),
            screen_y=e.args.get('screen_y'),
            client_x=e.args.get('client_x'),
            client_y=e.args.get('client_y'),
            offset_x=e.args.get('offset_x'),
            offset_y=e.args.get('offset_y'),
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

    def _handle_transform(self, e: GenericEventArguments) -> None:
        arguments = SceneTransformEventArguments(
            sender=self,
            client=self.client,
            type=e.args['type'],
            object_id=e.args['object_id'],
            object_name=e.args.get('object_name', ''),
            x=e.args['x'],
            y=e.args['y'],
            z=e.args['z'],
            rx=e.args['rx'],
            ry=e.args['ry'],
            rz=e.args['rz'],
            mode=e.args['mode'],
            wx=e.args.get('wx'),
            wy=e.args.get('wy'),
            wz=e.args.get('wz'),
        )
        if arguments.type == 'transform':
            handlers = self._transform_handlers
        elif arguments.type == 'transform_start':
            handlers = self._transform_start_handlers
        else:
            handlers = self._transform_end_handlers
        for handler in handlers:
            handle_event(handler, arguments)

    def enable_transform_controls(self,
                                  object_id: str,
                                  mode: Literal['translate', 'rotate', 'scale'] = 'translate',
                                  size: float | None = None,
                                  visible_axes: list[Literal['X', 'Y', 'Z']] | None = None,
                                  ) -> None:
        """Enable TransformControls gizmo on an object.

        :param object_id: ID of the object to attach transform controls to
        :param mode: transform mode - ``'translate'``, ``'rotate'``, or ``'scale'``
        :param size: optional gizmo size multiplier
        :param visible_axes: list of axes to show (e.g. ``['X']`` for X-only). If ``None``, shows all axes.
        """
        self.run_method('enable_transform_controls', object_id, mode, size, visible_axes)

    def disable_transform_controls(self, object_id: str) -> None:
        """Disable TransformControls gizmo on an object.

        :param object_id: ID of the object to detach transform controls from
        """
        self.run_method('disable_transform_controls', object_id)

    def set_transform_mode(self, object_id: str, mode: Literal['translate', 'rotate', 'scale']) -> None:
        """Change the transform mode of an object's gizmo.

        :param object_id: ID of the object with transform controls
        :param mode: transform mode - ``'translate'``, ``'rotate'``, or ``'scale'``
        """
        self.run_method('set_transform_mode', object_id, mode)

    def set_transform_size(self, object_id: str, size: float) -> None:
        """Change the size of an object's transform gizmo.

        :param object_id: ID of the object with transform controls
        :param size: gizmo size multiplier
        """
        self.run_method('set_transform_size', object_id, size)

    def set_transform_space(self, object_id: str, space: Literal['local', 'world']) -> None:
        """Set the transform space of an object's gizmo.

        :param object_id: ID of the object with transform controls
        :param space: ``'local'`` or ``'world'``
        """
        self.run_method('set_transform_space', object_id, space)

    def set_transform_rotation_snap(self, object_id: str, radians: float) -> None:
        """Set rotation snapping for an object's transform gizmo.

        :param object_id: ID of the object with transform controls
        :param radians: snap angle in radians (e.g. ``0.0873`` for 5 degrees)
        """
        self.run_method('set_transform_rotation_snap', object_id, radians)

    async def has_transform_controls(self, object_id: str) -> bool:
        """Check whether an object currently has TransformControls attached.

        :param object_id: ID of the object to check
        :return: ``True`` if TransformControls are attached, ``False`` otherwise
        """
        return await self.run_method('has_transform_controls', object_id)

    def set_transform_axis_colors(self,
                                  object_id: str,
                                  x: int | None = None,
                                  y: int | None = None,
                                  z: int | None = None,
                                  ) -> None:
        """Update TransformControls axis colors.

        :param object_id: ID of the object with transform controls
        :param x: hex color for the X axis (e.g. ``0xff0000`` for red)
        :param y: hex color for the Y axis (e.g. ``0x00ff00`` for green)
        :param z: hex color for the Z axis (e.g. ``0x0000ff`` for blue)
        """
        color_map: dict[str, int] = {}
        if x is not None:
            color_map['x'] = x
        if y is not None:
            color_map['y'] = y
        if z is not None:
            color_map['z'] = z
        self.run_method('set_transform_axis_colors', object_id, color_map)

    def set_orbit_enabled(self, flag: bool) -> None:
        """Enable or disable OrbitControls interaction.

        :param flag: ``True`` to enable orbit controls, ``False`` to disable
        """
        self.run_method('set_orbit_enabled', flag)

    def set_axes_inset(self, opts: dict[str, Any]) -> None:
        """Configure the orientation inset overlay.

        ``opts`` keys:
          - ``enabled``: bool (default ``False``)
          - ``size``: int (pixels)
          - ``margin``: int (pixels, used if ``marginX`` / ``marginY`` omitted)
          - ``marginX``: int (pixels)
          - ``marginY``: int (pixels)
          - ``anchor``: ``'bottom-left'`` | ``'bottom-right'`` | ``'top-left'`` | ``'top-right'``
        """
        self.run_method('set_axes_inset', opts)

    def set_axes_labels(self, opts: dict[str, Any]) -> None:
        """Configure axis labels for the orientation inset.

        ``opts`` keys:
          - ``enabled``: bool (default ``False``)
          - ``font``: CSS font string (e.g. ``'bold 32px sans-serif'``)
          - ``colorX``, ``colorY``, ``colorZ``: CSS colors
          - ``size``: sprite scale (default ``0.35``)
        """
        self.run_method('set_axes_labels', opts)

    def set_clipping_planes(self, object_id: str, planes: list[SceneClipPlane]) -> None:
        """Set clipping planes for an object (for proximity-based visibility).

        :param object_id: ID of the object to apply clipping to
        :param planes: list of :class:`SceneClipPlane` instances defining the clipping planes

        Example: to clip everything below Z=0.1::

            scene.set_clipping_planes('my_sphere', [SceneClipPlane(nx=0, ny=0, nz=1, d=-0.1)])
        """
        plane_dicts = [{'nx': p.nx, 'ny': p.ny, 'nz': p.nz, 'd': p.d} for p in planes]
        self.run_method('set_clipping_planes', object_id, plane_dicts)

    def clear_clipping_planes(self, object_id: str) -> None:
        """Clear clipping planes from an object.

        :param object_id: ID of the object to remove clipping from
        """
        self.run_method('clear_clipping_planes', object_id)

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
