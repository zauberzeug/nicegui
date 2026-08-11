from __future__ import annotations

import inspect
import math
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Literal

from typing_extensions import Self

from ... import binding
from ...awaitable_response import AwaitableResponse
from ...dependencies import register_library
from ...helpers import warn_once
from ...version import __version__

if TYPE_CHECKING:
    from .scene import Scene, SceneObject


class Object3D:
    current_scene: Scene | None = None
    EULER_ORDERS = ('XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX')

    _component_url: ClassVar[str | None] = None
    _file_stem: ClassVar[str | None] = None

    def __init_subclass__(cls, *, component: str | Path | None = None) -> None:  # DEPRECATED: require `component` in NiceGUI 4.0
        super().__init_subclass__()

        if component:
            path = Path(component)
            if not path.is_absolute():
                path = Path(inspect.getfile(cls)).parent / path
            if not path.is_file():
                raise ValueError(f'`component` must be an existing file, but "{component}" was not found')
            qualname = cls.__qualname__.replace('<locals>.', '')  # keep classes of different scopes apart
            import_name = f'{cls.__module__}.{qualname}'.replace('.', '__')
            library = register_library(path, import_name=import_name, max_time=path.stat().st_mtime)
            # Importing by URL rather than by importmap entry keeps classes registered after page render working.
            cls._component_url = f'/_nicegui/{__version__}/libraries/{library.key}'
            cls._file_stem = path.stem
        else:
            # Fallback to parent's component to ease inheriting from Object3D classes
            for base_cls in cls.__mro__[1:]:
                if getattr(base_cls, '_component_url', False):
                    break
            else:
                warn_once('Subclassing Object3D without a `component` parameter is deprecated '
                          'and will raise a TypeError in NiceGUI 4.0. '
                          'Pass `component=` or inherit from a built-in scene object instead.')

    def __init__(self, *args: Any, wireframe: bool = False) -> None:
        if self._component_url is None:
            args, wireframe = self._consume_legacy_type_string(args, wireframe)
        self.id = str(uuid.uuid4())
        self.wireframe = wireframe
        self.name: str | None = None
        assert self.current_scene is not None
        self.scene: Scene = self.current_scene
        self.scene.objects[self.id] = self
        self.parent: Object3D | SceneObject = self.scene.stack[-1]
        self.args: list = list(args)
        self.color: str | None = '#ffffff'
        self.opacity: float = 1.0
        self.side_: str = 'front'
        self.material_is_set: bool = False
        self.visible_: bool = True
        self.draggable_: bool = False
        self.x: float = 0
        self.y: float = 0
        self.z: float = 0
        self.R: list[list[float]] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.sx: float = 1
        self.sy: float = 1
        self.sz: float = 1
        self._create()

    # DEPRECATED: remove this method in NiceGUI 4.0
    def _consume_legacy_type_string(self, args: tuple, wireframe: bool) -> tuple[tuple, bool]:
        """Support the legacy protocol of instantiating an `Object3D` with a leading type string (until NiceGUI 4.0).

        The legacy protocol also passed the wireframe flag as the last positional argument of geometry-based types.
        """
        # pylint: disable=protected-access
        if not args or not isinstance(args[0], str):
            raise TypeError(f'Cannot create a {type(self).__name__} without a JS component. '
                            'Pass `component=` when subclassing Object3D.')
        subclasses = list(Object3D.__subclasses__())
        for subclass in subclasses:
            subclasses.extend(subclass.__subclasses__())
            if subclass._file_stem == args[0] and subclass._component_url:
                break
        else:
            raise TypeError(f'Unknown object type "{args[0]}".')
        warn_once(f'Creating 3D objects by passing a type string like "{args[0]}" to Object3D is deprecated '
                  'and will raise a TypeError in NiceGUI 4.0. '
                  'Subclass a built-in scene object or pass `component=` instead.')
        self._component_url = subclass._component_url  # type: ignore[misc]
        self._file_stem = subclass._file_stem  # type: ignore[misc]
        args = args[1:]
        geometry_types = ('box', 'sphere', 'cylinder', 'ring', 'quadratic_bezier_tube', 'extrusion')
        if self._file_stem in geometry_types and args and isinstance(args[-1], bool):
            wireframe = args[-1]
            args = args[:-1]
        return args, wireframe

    def with_name(self, name: str) -> Self:
        """Set the name of the object."""
        self.name = name
        self._name()
        return self

    @property
    def type(self) -> str | None:
        """Type of the object.

        **Note: This property is deprecated and will be removed in NiceGUI 4.0.
        Use `isinstance` checks instead.**
        """
        # DEPRECATED: remove this property in NiceGUI 4.0
        warn_once('The `type` property of `Object3D` is deprecated and will be removed in NiceGUI 4.0. '
                  'Use `isinstance` checks instead.')
        return self._file_stem

    @property
    def data(self) -> list[Any]:
        """Data to be sent to the frontend.

        **Note: This property is deprecated and will be removed in NiceGUI 4.0.
        It is a public method meant for internal use and is no longer needed.**
        """
        # DEPRECATED: remove this property in NiceGUI 4.0
        warn_once('The `data` property of `Object3D` is deprecated and will be removed in NiceGUI 4.0. '
                  'It is a public method meant for internal use and is no longer needed.')
        return [
            self._file_stem, self.id, self.parent.id, self.args,
            self.name,
            self.color, self.opacity, self.side_, self.material_is_set,
            self.x, self.y, self.z,
            self.R,
            self.sx, self.sy, self.sz,
            self.visible_,
            self.draggable_,
        ]

    def __enter__(self) -> Self:
        self.scene.stack.append(self)
        return self

    def __exit__(self, *_) -> None:
        self.scene.stack.pop()

    def _create(self) -> None:
        self.scene.run_method('create', self._component_url, self.id, self.parent.id, self.wireframe, *self.args)

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

    def _delete(self) -> None:
        self.scene.run_method('delete', self.id)

    def _resend(self) -> None:
        """Re-send the object to the client, e.g. after the scene was re-initialized due to WebGL context loss."""
        self._create()
        self._move()
        self._rotate()
        self._scale()
        if self.name:
            self._name()
        # Only override a component's own materials, like the ones of a GLTF model, if the user set one (#6118).
        if self.material_is_set:
            self._material()
        if not self.visible_:
            self._visible()
        if self.draggable_:
            self._draggable()

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
        if self.color != color or self.opacity != opacity or self.side_ != side or not self.material_is_set:
            self.color = color
            self.opacity = opacity
            self.side_ = side
            self.material_is_set = True
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
    def rotation_matrix_from_euler(
        r_x: float,
        r_y: float,
        r_z: float,
        order: Literal['XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX'] = 'XYZ',
    ) -> list[list[float]]:
        """Create a rotation matrix from Euler angles.

        The leftmost letter of ``order`` is the axis that rotates first about the world frame,
        the rightmost letter rotates last. For ``order='XYZ'`` the result is ``M = Rz @ Ry @ Rx``,
        which preserves the original three-argument behavior of this function.

        Note: this is the *reverse* of the ``THREE.Euler`` order convention. ``rotate(rx, ry, rz, 'ABC')``
        is equivalent to ``new THREE.Euler(rx, ry, rz, 'CBA')`` (order string reversed).

        :param r_x: rotation around the x axis in radians
        :param r_y: rotation around the y axis in radians
        :param r_z: rotation around the z axis in radians
        :param order: Euler rotation order (``'XYZ'`` | ``'XZY'`` | ``'YXZ'`` | ``'YZX'`` | ``'ZXY'`` | ``'ZYX'``, default ``'XYZ'``)
        """
        if order not in Object3D.EULER_ORDERS:
            raise ValueError(f'Unsupported Euler order {order!r}; expected one of {", ".join(Object3D.EULER_ORDERS)}')
        sx, cx = math.sin(r_x), math.cos(r_x)
        sy, cy = math.sin(r_y), math.cos(r_y)
        sz, cz = math.sin(r_z), math.cos(r_z)
        single_axis: dict[str, list[list[float]]] = {
            'X': [[1, 0, 0], [0, cx, -sx], [0, sx, cx]],
            'Y': [[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]],
            'Z': [[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]],
        }
        # Each letter pre-multiplies on the left, so order='XYZ' yields Rz @ Ry @ Rx (Rx applied first).
        result = single_axis[order[0]]
        for letter in order[1:]:
            result = Object3D._matmul3(single_axis[letter], result)
        return result

    @staticmethod
    def _matmul3(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
        return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

    def rotate(
        self,
        r_x: float,
        r_y: float,
        r_z: float,
        order: Literal['XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX'] = 'XYZ',
    ) -> Self:
        """Rotate the object.

        The leftmost letter of ``order`` rotates first about the world frame
        (default ``'XYZ'`` preserves the original three-argument behavior, ``M = Rz @ Ry @ Rx``).
        See :meth:`rotation_matrix_from_euler` for the relationship to ``THREE.Euler``.

        :param r_x: rotation around the x axis in radians
        :param r_y: rotation around the y axis in radians
        :param r_z: rotation around the z axis in radians
        :param order: Euler rotation order (``'XYZ'`` | ``'XZY'`` | ``'YXZ'`` | ``'YZX'`` | ``'ZXY'`` | ``'ZYX'``, default ``'XYZ'``)
        """
        return self.rotate_R(self.rotation_matrix_from_euler(r_x, r_y, r_z, order))

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

    @property
    def ancestors(self) -> list[Object3D]:
        """List of ancestors of the object, from the direct parent up to the root.

        *Added in version 3.16.0*
        """
        ancestors: list[Object3D] = []
        parent = self.parent
        while isinstance(parent, Object3D):
            ancestors.append(parent)
            parent = parent.parent
        return ancestors

    def delete(self) -> None:
        """Delete the object."""
        for child in self.children:
            child.delete()
        del self.scene.objects[self.id]
        binding.remove([self])
        self._delete()

    def run_method(self, name: str, *args: Any, timeout: float = 1) -> AwaitableResponse:
        """Run a method on the JS component on the client side.

        If the function is awaited, the result of the method call is returned.
        Otherwise, the method is executed without waiting for a response.

        Note that the client dispatches the call only once the object has been created.
        When awaiting a result right after creating an object with a slow-loading component
        (e.g. a large glTF model), you may need to increase the ``timeout``.

        *Added in version 3.16.0*

        :param name: name of the method
        :param args: arguments to pass to the method
        :param timeout: maximum time to wait for a response (default: 1 second)
        """
        return self.scene.run_method('run_method_on_component', self.id, name, *args, timeout=timeout)
