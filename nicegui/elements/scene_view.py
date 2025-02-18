import asyncio
from typing import Optional

from typing_extensions import Self

from ..element import Element
from ..events import (
    ClickEventArguments,
    GenericEventArguments,
    Handler,
    SceneClickEventArguments,
    SceneClickHit,
    handle_event,
)
from .scene import Scene, SceneCamera


class SceneView(Element,
                component='scene_view.js',
                dependencies=[
                    'lib/tween/tween.umd.js',
                    'lib/three/three.module.js',
                ],
                default_classes='nicegui-scene-view'):

    def __init__(self,
                 scene: Scene,
                 width: int = 400,
                 height: int = 300,
                 camera: Optional[SceneCamera] = None,
                 on_click: Optional[Handler[ClickEventArguments]] = None,
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
        """
        super().__init__()
        self._props['width'] = width
        self._props['height'] = height
        self._props['scene_id'] = scene.id
        self.camera = camera or Scene.perspective_camera()
        self._props['camera_type'] = self.camera.type
        self._props['camera_params'] = self.camera.params
        self._click_handlers = [on_click] if on_click else []
        self.on('init', self._handle_init)
        self.on('click3d', self._handle_click)

    def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
        """Add a callback to be invoked when a 3D object is clicked."""
        self._click_handlers.append(callback)
        return self

    def _handle_init(self, e: GenericEventArguments) -> None:
        with self.client.individual_target(e.args['socket_id']):
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
