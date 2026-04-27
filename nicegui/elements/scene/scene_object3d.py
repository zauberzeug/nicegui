from __future__ import annotations

import math
import uuid
from typing import TYPE_CHECKING, Any, Literal

from typing_extensions import Self

from ...events import Handler, ScenePointerEventArguments

if TYPE_CHECKING:
    from .scene import Scene, SceneObject


# JS-side event type names (the strings the JS emits in the "pointerevent" payload's `type` field).
# Each Python chain method maps to exactly one of these.
_POINTER_EVENT_TYPES = (
    'pointerover', 'pointerout', 'pointerdown', 'pointerup',
    'pointermove', 'click', 'dblclick', 'contextmenu',
)


class Object3D:
    current_scene: Scene | None = None

    def __init__(self, type_: str, *args: Any) -> None:
        self.type = type_
        self.id = str(uuid.uuid4())
        self.name: str | None = None
        assert self.current_scene is not None
        self.scene: Scene = self.current_scene
        self.scene.objects[self.id] = self
        self.parent: Object3D | SceneObject = self.scene.stack[-1]
        self.args: list = list(args)
        self.color: str | None = '#ffffff'
        self.opacity: float = 1.0
        self.side_: str = 'front'
        self.visible_: bool = True
        self.draggable_: bool = False
        self.x: float = 0
        self.y: float = 0
        self.z: float = 0
        self.R: list[list[float]] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.sx: float = 1
        self.sy: float = 1
        self.sz: float = 1
        # Per-object pointer event handler lists. An object becomes "interactive" on the JS side
        # (joins the raycast list) iff at least one of these lists is non-empty or _effect_spec is set.
        self._pointer_handlers: dict[str, list[Handler[ScenePointerEventArguments]]] = {
            event_type: [] for event_type in _POINTER_EVENT_TYPES
        }
        self._effect_spec: dict[str, Any] | None = None
        self._create()

    def with_name(self, name: str) -> Self:
        """Set the name of the object."""
        self.name = name
        self._name()
        return self

    @property
    def data(self) -> list[Any]:
        """Data to be sent to the frontend."""
        result: list[Any] = [
            self.type, self.id, self.parent.id, self.args,
            self.name,
            self.color, self.opacity, self.side_,
            self.x, self.y, self.z,
            self.R,
            self.sx, self.sy, self.sz,
            self.visible_,
            self.draggable_,
        ]
        # Append the interactive state only when truthy. The JS unpacker uses array destructuring
        # and treats a missing trailing field as `undefined`, so default objects stay length-stable.
        interactive = self._build_interactive_payload()
        if interactive:
            result.append(interactive)
        return result

    def _build_interactive_payload(self) -> dict[str, Any] | None:
        active_handler_types = [event_type for event_type, handlers in self._pointer_handlers.items() if handlers]
        if not active_handler_types and self._effect_spec is None:
            return None
        payload: dict[str, Any] = {}
        if active_handler_types:
            payload['handlers'] = active_handler_types
        if self._effect_spec is not None:
            payload['effect'] = self._effect_spec
        return payload

    def __enter__(self) -> Self:
        self.scene.stack.append(self)
        return self

    def __exit__(self, *_) -> None:
        self.scene.stack.pop()

    def _create(self) -> None:
        self.scene.run_method('create', self.type, self.id, self.parent.id, *self.args)

    def _name(self) -> None:
        self.scene.run_method('name', self.id, self.name)

    def _material(self) -> None:
        self.scene.run_method('material', self.id, self.color, self.opacity, self.side_)

    def _move(self) -> None:
        self.scene.run_method('move', self.id, self.x, self.y, self.z)

    def _rotate(self) -> None:
        self.scene.run_method('rotate', self.id, self.R)

    def _scale(self) -> None:
        self.scene.run_method('scale', self.id, self.sx, self.sy, self.sz)

    def _visible(self) -> None:
        self.scene.run_method('visible', self.id, self.visible_)

    def _draggable(self) -> None:
        self.scene.run_method('draggable', self.id, self.draggable_)

    def _sync_handler_types(self) -> None:
        """Push the current set of registered handler types to the JS side."""
        active = [event_type for event_type, handlers in self._pointer_handlers.items() if handlers]
        self.scene.run_method('set_handler_types', self.id, active)

    def _sync_effect(self) -> None:
        """Push the current effect spec to the JS side."""
        if self._effect_spec is None:
            self.scene.run_method('set_effect', self.id, None, None)
        else:
            self.scene.run_method(
                'set_effect', self.id,
                self._effect_spec.get('effect'),
                self._effect_spec.get('color'),
            )

    def _delete(self) -> None:
        self.scene.run_method('delete', self.id)

    def material(self,
                 color: str | None = '#ffffff',
                 opacity: float = 1.0,
                 side: Literal['front', 'back', 'both'] = 'front',
                 ) -> Self:
        """Set the color and opacity of the object.

        :param color: CSS color string (default: '#ffffff')
        :param opacity: opacity between 0.0 and 1.0 (default: 1.0)
        :param side: 'front', 'back', or 'double' (default: 'front')
        """
        if self.color != color or self.opacity != opacity or self.side_ != side:
            self.color = color
            self.opacity = opacity
            self.side_ = side
            self._material()
        return self

    def move(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Self:
        """Move the object.

        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        """
        if self.x != x or self.y != y or self.z != z:
            self.x = x
            self.y = y
            self.z = z
            self._move()
        return self

    @staticmethod
    def rotation_matrix_from_euler(r_x: float, r_y: float, r_z: float) -> list[list[float]]:
        """Create a rotation matrix from Euler angles.

        :param r_x: rotation around the x axis in radians
        :param r_y: rotation around the y axis in radians
        :param r_z: rotation around the z axis in radians
        """
        sx, cx = math.sin(r_x), math.cos(r_x)
        sy, cy = math.sin(r_y), math.cos(r_y)
        sz, cz = math.sin(r_z), math.cos(r_z)
        return [
            [cz * cy, -sz * cx + cz * sy * sx, sz * sx + cz * sy * cx],
            [sz * cy, cz * cx + sz * sy * sx, -cz * sx + sz * sy * cx],
            [-sy, cy * sx, cy * cx],
        ]

    def rotate(self, r_x: float, r_y: float, r_z: float) -> Self:
        """Rotate the object.

        :param r_x: rotation around the x axis in radians
        :param r_y: rotation around the y axis in radians
        :param r_z: rotation around the z axis in radians
        """
        return self.rotate_R(self.rotation_matrix_from_euler(r_x, r_y, r_z))

    def rotate_R(self, R: list[list[float]]) -> Self:
        """Rotate the object.

        :param R: 3x3 rotation matrix
        """
        if self.R != R:
            self.R = R
            self._rotate()
        return self

    def scale(self, sx: float = 1.0, sy: float | None = None, sz: float | None = None) -> Self:
        """Scale the object.

        :param sx: scale factor for the x axis
        :param sy: scale factor for the y axis (default: `sx`)
        :param sz: scale factor for the z axis (default: `sx`)
        """
        if sy is None:
            sy = sx
        if sz is None:
            sz = sx
        if self.sx != sx or self.sy != sy or self.sz != sz:
            self.sx = sx
            self.sy = sy
            self.sz = sz
            self._scale()
        return self

    def visible(self, value: bool = True) -> Self:
        """Set the visibility of the object.

        :param value: whether the object should be visible (default: `True`)
        """
        if self.visible_ != value:
            self.visible_ = value
            self._visible()
        return self

    def draggable(self, value: bool = True) -> Self:
        """Set whether the object should be draggable.

        :param value: whether the object should be draggable (default: `True`)
        """
        if self.draggable_ != value:
            self.draggable_ = value
            self._draggable()
        return self

    def _add_pointer_handler(self,
                             event_type: str,
                             callback: Handler[ScenePointerEventArguments],
                             ) -> Self:
        """Append a callback to the per-object handler list for ``event_type`` and sync to JS.

        When this is the first handler for the object (and no effect is set), the JS side
        adds the underlying three.js object to its raycast list so future pointer events
        can be detected and dispatched.
        """
        was_empty = not any(self._pointer_handlers.values()) and self._effect_spec is None
        first_for_type = not self._pointer_handlers[event_type]
        self._pointer_handlers[event_type].append(callback)
        if was_empty or first_for_type:
            self._sync_handler_types()
        return self

    def on_pointer_over(self, callback: Handler[ScenePointerEventArguments]) -> Self:
        """Add a callback fired when the cursor enters this object's hit volume.

        *added in version X.Y.Z*
        """
        return self._add_pointer_handler('pointerover', callback)

    def on_pointer_out(self, callback: Handler[ScenePointerEventArguments]) -> Self:
        """Add a callback fired when the cursor leaves this object's hit volume.

        *added in version X.Y.Z*
        """
        return self._add_pointer_handler('pointerout', callback)

    def on_pointer_down(self, callback: Handler[ScenePointerEventArguments]) -> Self:
        """Add a callback fired when a mouse button is pressed while the cursor is over this object.

        *added in version X.Y.Z*
        """
        return self._add_pointer_handler('pointerdown', callback)

    def on_pointer_up(self, callback: Handler[ScenePointerEventArguments]) -> Self:
        """Add a callback fired when a mouse button is released while the cursor is over this object.

        *added in version X.Y.Z*
        """
        return self._add_pointer_handler('pointerup', callback)

    def on_pointer_move(self, callback: Handler[ScenePointerEventArguments]) -> Self:
        """Add a callback fired while the cursor moves over this object.

        Note: this is a high-frequency event. Emissions are throttled to ~60Hz on the client,
        but Python handlers should still expect many invocations per second during a drag.
        Debounce before pushing to expensive sinks.

        *added in version X.Y.Z*
        """
        return self._add_pointer_handler('pointermove', callback)

    def on_click(self, callback: Handler[ScenePointerEventArguments]) -> Self:
        """Add a callback fired when this specific object is clicked.

        Per-object click is additive to :meth:`Scene.on_click` (the scene-level any-click handler);
        both fire on a click that hits this object.

        *added in version X.Y.Z*
        """
        return self._add_pointer_handler('click', callback)

    def on_double_click(self, callback: Handler[ScenePointerEventArguments]) -> Self:
        """Add a callback fired when this specific object is double-clicked.

        *added in version X.Y.Z*
        """
        return self._add_pointer_handler('dblclick', callback)

    def on_context_menu(self, callback: Handler[ScenePointerEventArguments]) -> Self:
        """Add a callback fired when this specific object is right-clicked.

        *added in version X.Y.Z*
        """
        return self._add_pointer_handler('contextmenu', callback)

    def hover_effect(self,
                     effect: Literal['glow', 'outline', 'tint', 'none'] | bool = 'glow',
                     *,
                     color: str | None = None,
                     ) -> Self:
        """Apply a client-side visual effect when the cursor hovers over this object.

        The effect runs entirely on the client — no Python round-trip per hover state change
        for the visual itself. Pass ``False`` or ``'none'`` to disable.

        :param effect: ``'glow'`` (back-face mesh clone), ``'outline'`` (edges geometry),
            ``'tint'`` (emissive color), or ``'none'`` / ``False`` to disable
        :param color: optional CSS color string; if omitted, falls back to the scene-level
            ``hover_color`` constructor argument

        For ``'glow'``, the scene-level ``hover_opacity`` and ``hover_scale`` constructor
        arguments tune the appearance. ``'outline'`` and ``'tint'`` ignore those parameters.

        *added in version X.Y.Z*
        """
        if effect is False or effect == 'none':
            new_spec: dict[str, Any] | None = None
        else:
            new_spec = {'effect': effect, 'color': color}
        if self._effect_spec == new_spec:
            return self
        self._effect_spec = new_spec
        self._sync_effect()
        return self

    def enable_transform_controls(self,
                                  *,
                                  mode: Literal['translate', 'rotate', 'scale'] = 'translate',
                                  size: float | None = None,
                                  visible_axes: list[Literal['X', 'Y', 'Z']] | None = None,
                                  space: Literal['local', 'world'] | None = None,
                                  rotation_snap: float | None = None,
                                  ) -> Self:
        """Attach a TransformControls gizmo so the user can drag this object in 3D.

        Drag events are emitted on the parent :class:`ui.scene` via the ``on_transform``,
        ``on_transform_start``, and ``on_transform_end`` callbacks.

        :param mode: gizmo mode (``'translate'``, ``'rotate'``, or ``'scale'``, default: ``'translate'``)
        :param size: optional gizmo size multiplier
        :param visible_axes: list of axes to show (e.g. ``['X']`` for X-only); shows all axes if ``None``
        :param space: ``'local'`` or ``'world'`` (defaults to three.js' ``'world'``)
        :param rotation_snap: optional snap angle in radians (e.g. ``math.radians(5)``)

        *added in version X.Y.Z*
        """
        self.scene.run_method('enable_transform_controls', self.id, mode, size, visible_axes, space, rotation_snap)
        return self

    def disable_transform_controls(self) -> Self:
        """Detach the TransformControls gizmo from this object.

        *added in version X.Y.Z*
        """
        self.scene.run_method('disable_transform_controls', self.id)
        return self

    def set_transform_mode(self, mode: Literal['translate', 'rotate', 'scale']) -> Self:
        """Change this object's TransformControls mode.

        *added in version X.Y.Z*
        """
        self.scene.run_method('set_transform_mode', self.id, mode)
        return self

    def set_transform_size(self, size: float) -> Self:
        """Change this object's TransformControls gizmo size.

        *added in version X.Y.Z*
        """
        self.scene.run_method('set_transform_size', self.id, size)
        return self

    def set_transform_space(self, space: Literal['local', 'world']) -> Self:
        """Change this object's TransformControls coordinate space.

        *added in version X.Y.Z*
        """
        self.scene.run_method('set_transform_space', self.id, space)
        return self

    def set_transform_rotation_snap(self, radians: float) -> Self:
        """Change this object's TransformControls rotation snap angle in radians.

        *added in version X.Y.Z*
        """
        self.scene.run_method('set_transform_rotation_snap', self.id, radians)
        return self

    def attach(self, parent: Object3D) -> None:
        """Attach the object to a parent object.

        The position and rotation of the object are preserved so that the object does not move in space.

        But note that scaling is not preserved.
        If either the parent or the object itself is scaled, the object shape and position can change.

        *Added in version 2.7.0*
        """
        self.detach()
        self.parent = parent
        self._move_into_parent(parent)
        self.scene.run_method('attach', self.id, parent.id, self.x, self.y, self.z, self.R)

    def _move_into_parent(self, parent: Object3D | SceneObject) -> None:
        if not isinstance(parent, Object3D):
            return
        if isinstance(parent.parent, Object3D):
            self._move_into_parent(parent.parent)
        M1: list[list[float]] = [
            [self.R[0][0], self.R[0][1], self.R[0][2], self.x],
            [self.R[1][0], self.R[1][1], self.R[1][2], self.y],
            [self.R[2][0], self.R[2][1], self.R[2][2], self.z],
            [0, 0, 0, 1],
        ]
        M2_inv: list[list[float]] = [
            [parent.R[0][0], parent.R[1][0], parent.R[2][0],
             - parent.R[0][0] * parent.x
             - parent.R[1][0] * parent.y
             - parent.R[2][0] * parent.z],
            [parent.R[0][1], parent.R[1][1], parent.R[2][1],
             - parent.R[0][1] * parent.x
             - parent.R[1][1] * parent.y
             - parent.R[2][1] * parent.z],
            [parent.R[0][2], parent.R[1][2], parent.R[2][2],
             - parent.R[0][2] * parent.x
             - parent.R[1][2] * parent.y
             - parent.R[2][2] * parent.z],
            [0, 0, 0, 1],
        ]
        M: list[list[float]] = [
            [
                M2_inv[0][0] * M1[0][0] + M2_inv[0][1] * M1[1][0] + M2_inv[0][2] * M1[2][0],
                M2_inv[0][0] * M1[0][1] + M2_inv[0][1] * M1[1][1] + M2_inv[0][2] * M1[2][1],
                M2_inv[0][0] * M1[0][2] + M2_inv[0][1] * M1[1][2] + M2_inv[0][2] * M1[2][2],
                M2_inv[0][0] * M1[0][3] + M2_inv[0][1] * M1[1][3] + M2_inv[0][2] * M1[2][3] + M2_inv[0][3],
            ],
            [
                M2_inv[1][0] * M1[0][0] + M2_inv[1][1] * M1[1][0] + M2_inv[1][2] * M1[2][0],
                M2_inv[1][0] * M1[0][1] + M2_inv[1][1] * M1[1][1] + M2_inv[1][2] * M1[2][1],
                M2_inv[1][0] * M1[0][2] + M2_inv[1][1] * M1[1][2] + M2_inv[1][2] * M1[2][2],
                M2_inv[1][0] * M1[0][3] + M2_inv[1][1] * M1[1][3] + M2_inv[1][2] * M1[2][3] + M2_inv[1][3],
            ],
            [
                M2_inv[2][0] * M1[0][0] + M2_inv[2][1] * M1[1][0] + M2_inv[2][2] * M1[2][0],
                M2_inv[2][0] * M1[0][1] + M2_inv[2][1] * M1[1][1] + M2_inv[2][2] * M1[2][1],
                M2_inv[2][0] * M1[0][2] + M2_inv[2][1] * M1[1][2] + M2_inv[2][2] * M1[2][2],
                M2_inv[2][0] * M1[0][3] + M2_inv[2][1] * M1[1][3] + M2_inv[2][2] * M1[2][3] + M2_inv[2][3],
            ],
            [
                0, 0, 0, 1,
            ],
        ]
        self.x = M[0][3]
        self.y = M[1][3]
        self.z = M[2][3]
        self.R = [
            [M[0][0], M[0][1], M[0][2]],
            [M[1][0], M[1][1], M[1][2]],
            [M[2][0], M[2][1], M[2][2]],
        ]

    def detach(self) -> None:
        """Remove the object from its parent group object.

        The position and rotation of the object are preserved so that the object does not move in space.

        But note that scaling is not preserved.
        If either the parent or the object itself is scaled, the object shape and position can change.

        *Added in version 2.7.0*
        """
        self._move_out_of_parent(self.parent)
        self.parent = self.scene.stack[0]
        self.scene.run_method('detach', self.id, self.x, self.y, self.z, self.R)

    def _move_out_of_parent(self, parent: Object3D | SceneObject) -> None:
        if not isinstance(parent, Object3D):
            return
        M1: list[list[float]] = [
            [self.R[0][0], self.R[0][1], self.R[0][2], self.x],
            [self.R[1][0], self.R[1][1], self.R[1][2], self.y],
            [self.R[2][0], self.R[2][1], self.R[2][2], self.z],
            [0, 0, 0, 1],
        ]
        M2: list[list[float]] = [
            [parent.R[0][0], parent.R[0][1], parent.R[0][2], parent.x],
            [parent.R[1][0], parent.R[1][1], parent.R[1][2], parent.y],
            [parent.R[2][0], parent.R[2][1], parent.R[2][2], parent.z],
            [0, 0, 0, 1],
        ]
        M: list[list[float]] = [
            [
                M2[0][0] * M1[0][0] + M2[0][1] * M1[1][0] + M2[0][2] * M1[2][0],
                M2[0][0] * M1[0][1] + M2[0][1] * M1[1][1] + M2[0][2] * M1[2][1],
                M2[0][0] * M1[0][2] + M2[0][1] * M1[1][2] + M2[0][2] * M1[2][2],
                M2[0][0] * M1[0][3] + M2[0][1] * M1[1][3] + M2[0][2] * M1[2][3] + M2[0][3],
            ],
            [
                M2[1][0] * M1[0][0] + M2[1][1] * M1[1][0] + M2[1][2] * M1[2][0],
                M2[1][0] * M1[0][1] + M2[1][1] * M1[1][1] + M2[1][2] * M1[2][1],
                M2[1][0] * M1[0][2] + M2[1][1] * M1[1][2] + M2[1][2] * M1[2][2],
                M2[1][0] * M1[0][3] + M2[1][1] * M1[1][3] + M2[1][2] * M1[2][3] + M2[1][3],
            ],
            [
                M2[2][0] * M1[0][0] + M2[2][1] * M1[1][0] + M2[2][2] * M1[2][0],
                M2[2][0] * M1[0][1] + M2[2][1] * M1[1][1] + M2[2][2] * M1[2][1],
                M2[2][0] * M1[0][2] + M2[2][1] * M1[1][2] + M2[2][2] * M1[2][2],
                M2[2][0] * M1[0][3] + M2[2][1] * M1[1][3] + M2[2][2] * M1[2][3] + M2[2][3],
            ],
            [
                0, 0, 0, 1,
            ],
        ]
        self.x = M[0][3]
        self.y = M[1][3]
        self.z = M[2][3]
        self.R = [
            [M[0][0], M[0][1], M[0][2]],
            [M[1][0], M[1][1], M[1][2]],
            [M[2][0], M[2][1], M[2][2]],
        ]
        if isinstance(parent.parent, Object3D):
            self._move_out_of_parent(parent.parent)

    @property
    def children(self) -> list[Object3D]:
        """List of children of the object.

        *Added in version 2.4.0*
        """
        return [object for object in self.scene.objects.values() if object.parent == self]

    def delete(self) -> None:
        """Delete the object."""
        for child in self.children:
            child.delete()
        del self.scene.objects[self.id]
        self._delete()
