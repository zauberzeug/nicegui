import uuid
from typing import TYPE_CHECKING, Any, List, Optional, Union, cast

import numpy as np

from .. import globals

if TYPE_CHECKING:
    from .scene import Scene, SceneObject


class Object3D:

    def __init__(self, type: str, *args: Any) -> None:
        self.type = type
        self.id = str(uuid.uuid4())
        self.name: Optional[str] = None
        self.scene: 'Scene' = cast('Scene', globals.get_slot().parent)
        self.scene.objects[self.id] = self
        self.parent: Union[Object3D, SceneObject] = self.scene.stack[-1]
        self.args: List = list(args)
        self.color: str = '#ffffff'
        self.opacity: float = 1.0
        self.side_: str = 'front'
        self.visible_: bool = True
        self.x: float = 0
        self.y: float = 0
        self.z: float = 0
        self.R: List[List[float]] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.sx: float = 1
        self.sy: float = 1
        self.sz: float = 1
        self._create()

    def with_name(self, name: str):
        self.name = name
        self._name()
        return self

    def send(self) -> None:
        self._create()
        self._name()
        self._material()
        self._move()
        self._rotate()
        self._scale()
        self._visible()

    def __enter__(self):
        self.scene.stack.append(self)
        return self

    def __exit__(self, *_):
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

    def _delete(self) -> None:
        self.scene.run_method('delete', self.id)

    def material(self, color: str = '#ffffff', opacity: float = 1.0, side: str = 'front'):
        if self.color != color or self.opacity != opacity or self.side_ != side:
            self.color = color
            self.opacity = opacity
            self.side_ = side
            self._material()
        return self

    def move(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        if self.x != x or self.y != y or self.z != z:
            self.x = x
            self.y = y
            self.z = z
            self._move()
        return self

    def rotate(self, omega: float, phi: float, kappa: float):
        Rx = np.array([[1, 0, 0], [0, np.cos(omega), -np.sin(omega)], [0, np.sin(omega), np.cos(omega)]])
        Ry = np.array([[np.cos(phi), 0, np.sin(phi)], [0, 1, 0], [-np.sin(phi), 0, np.cos(phi)]])
        Rz = np.array([[np.cos(kappa), -np.sin(kappa), 0], [np.sin(kappa), np.cos(kappa), 0], [0, 0, 1]])
        return self.rotate_R((Rz @ Ry @ Rx).tolist())

    def rotate_R(self, R: List[List[float]]):
        if self.R != R:
            self.R = R
            self._rotate()
        return self

    def scale(self, sx: float = 1.0, sy: Optional[float] = None, sz: Optional[float] = None):
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

    def visible(self, value: bool = True):
        if self.visible_ != value:
            self.visible_ = value
            self._visible()
        return self

    def delete(self) -> None:
        children = [object for object in self.scene.objects.values() if object.parent == self]
        for child in children:
            child.delete()
        del self.scene.objects[self.id]
        self._delete()
