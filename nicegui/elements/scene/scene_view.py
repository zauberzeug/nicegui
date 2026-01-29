import asyncio

from typing_extensions import Self

from ...defaults import DEFAULT_PROP, resolve_defaults
from ...element import Element
from ...events import (
    ClickEventArguments,
    GenericEventArguments,
    Handler,
    SceneClickEventArguments,
    SceneClickHit,
    handle_event,
)
from .scene import Scene, SceneCamera


class SceneView(Element, component='scene_view.js', default_classes='nicegui-scene-view'):
    # NOTE: The ESM is already registered in scene.py.

    @resolve_defaults
    def __init__(self,
                 scene: Scene,
                 # DEPRECATED: enforce keyword-only arguments in NiceGUI 4.0
                 width: int = DEFAULT_PROP | 400,
                 height: int = DEFAULT_PROP | 300,
                 camera: SceneCamera | None = None,
                 on_click: Handler[ClickEventArguments] | None = None,
                 fps: int = DEFAULT_PROP | 20,
                 show_stats: bool = DEFAULT_PROP | False,
                 ) -> None:
        """Scene View

        Display an additional view of a 3D scene using `three.js <https://threejs.org/>`_.
        This component can only show a scene and not modify it.
        You can, however, independently move the camera.

        Current limitation: 2D and 3D text objects are not supported and will not be displayed in the scene view.

        :param scene: the scene which will be shown on the canvas
        :param width: width of the canvas
        :param height: height of the canvas
        :param camera: camera definition, either instance of ``ui.scene.perspective_camera`` (default) or ``ui.scene.orthographic_camera``
        :param on_click: callback to execute when a 3D object is clicked
        :param fps: target frame rate for the scene view in frames per second (default: 20, *added in version 3.2.0*)
        :param show_stats: whether to show performance stats (default: ``False``, *added in version 3.2.0*)
        """
        super().__init__()
        self._props['width'] = width
        self._props['height'] = height
        self._props['fps'] = fps
        self._props['show-stats'] = show_stats
        self._props['scene-id'] = scene.id
        self.camera = camera or Scene.perspective_camera()
        self._props['camera-type'] = self.camera.type
        self._props['camera-params'] = self.camera.params
        self._click_handlers = [on_click] if on_click else []
        self.on('init', self._handle_init)
        self.on('click3d', self._handle_click)

        self._props.add_rename('camera_params', 'camera-params')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('camera_type', 'camera-type')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('scene_id', 'scene-id')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('show_stats', 'show-stats')  # DEPRECATED: remove in NiceGUI 4.0

    def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
        """Add a callback to be invoked when a 3D object is clicked."""
        self._click_handlers.append(callback)
        return self

    def _handle_init(self) -> None:
        self.move_camera(duration=0)
        self.run_method('init')

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
