from __future__ import annotations

import math
import uuid
from typing import TYPE_CHECKING, Any, List, Literal, Optional, Union

from typing_extensions import Self

if TYPE_CHECKING:
    from .scene import Scene, SceneObject


class Object3D:
    current_scene: Optional[Scene] = None

    def __init__(self, type_: str, *args: Any) -> None:
        self.type = type_
        self.id = str(uuid.uuid4())
        self.name: Optional[str] = None
        assert self.current_scene is not None
        self.scene: Scene = self.current_scene
        self.scene.objects[self.id] = self
        self.parent: Union[Object3D, SceneObject] = self.scene.stack[-1]
        self.args: List = list(args)
        self.color: str = '#ffffff'
        self.opacity: float = 1.0
        self.side_: str = 'front'
        self.visible_: bool = True
        self.draggable_: bool = False
        self.x: float = 0
        self.y: float = 0
        self.z: float = 0
        self.R: List[List[float]] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.sx: float = 1
        self.sy: float = 1
        self.sz: float = 1
        self._create()

    def with_name(self, name: str) -> Self:
        """Set the name of the object."""
        self.name = name
        self._name()
        return self

    @property
    def data(self) -> List[Any]:
        """Data to be sent to the frontend."""
        return [
            self.type, self.id, self.parent.id, self.args,
            self.name,
            self.color, self.opacity, self.side_,
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

    def _delete(self) -> None:
        self.scene.run_method('delete', self.id)

    def material(self, color: str = '#ffffff', opacity: float = 1.0, side: Literal['front', 'back', 'both'] = 'front') -> Self:
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
    def rotation_matrix_from_euler(r_x: float, r_y: float, r_z: float) -> List[List[float]]:
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

    def rotate_R(self, R: List[List[float]]) -> Self:
        """Rotate the object.

        :param R: 3x3 rotation matrix
        """
        if self.R != R:
            self.R = R
            self._rotate()
        return self

    def scale(self, sx: float = 1.0, sy: Optional[float] = None, sz: Optional[float] = None) -> Self:
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

    def delete(self) -> None:
        """Delete the object."""
        children = [object for object in self.scene.objects.values() if object.parent == self]
        for child in children:
            child.delete()
        del self.scene.objects[self.id]
        self._delete()
