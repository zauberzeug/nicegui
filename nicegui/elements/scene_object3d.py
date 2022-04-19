from __future__ import annotations

import uuid
from typing import List, Optional

import numpy as np
from justpy.htmlcomponents import WebPage

from ..task_logger import create_task


class Object3D:
    stack: List[Object3D] = []

    def __init__(self, type: str, *args):
        self.type = type
        self.id = str(uuid.uuid4())
        self.name = None
        self.parent = self.stack[-1]
        self.view = self.parent.view
        self.page = self.parent.page
        self.args = list(args)
        self.color = '#ffffff'
        self.opacity = 1.0
        self.side_: str = 'front'
        self.visible_: bool = True
        self.x = 0
        self.y = 0
        self.z = 0
        self.R = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.sx = 1
        self.sy = 1
        self.sz = 1
        self.run_command(self._create_command)
        self.view.objects[self.id] = self

    def with_name(self, name: str) -> Object3D:
        self.name = name
        return self

    def run_command(self, command: str, socket=None):
        sockets = [socket] if socket else WebPage.sockets.get(self.page.page_id, {}).values()
        for socket in sockets:
            create_task(self.view.run_method(command, socket), name=command)

    def send_to(self, socket):
        self.run_command(self._create_command, socket)
        self.run_command(self._material_command, socket)
        self.run_command(self._move_command, socket)
        self.run_command(self._rotate_command, socket)
        self.run_command(self._scale_command, socket)
        self.run_command(self._visible_command, socket)

    def __enter__(self):
        self.stack.append(self)
        return self

    def __exit__(self, *_):
        self.stack.pop()

    @property
    def _create_command(self):
        return f'create("{self.type}", "{self.id}", "{self.parent.id}", {str(self.args)[1:-1]})'

    @property
    def _material_command(self):
        return f'material("{self.id}", "{self.color}", "{self.opacity}", "{self.side_}")'

    @property
    def _move_command(self):
        return f'move("{self.id}", {self.x}, {self.y}, {self.z})'

    @property
    def _rotate_command(self):
        return f'rotate("{self.id}", {self.R})'

    @property
    def _scale_command(self):
        return f'scale("{self.id}", {self.sx}, {self.sy}, {self.sz})'

    @property
    def _visible_command(self):
        return f'visible("{self.id}", {self.visible_})'

    @property
    def _delete_command(self):
        return f'delete("{self.id}")'

    def material(self, color: str = '#ffffff', opacity: float = 1.0, side: str = 'front'):
        if self.color != color or self.opacity != opacity or self.side_ != side:
            self.color = color
            self.opacity = opacity
            self.side_ = side
            self.run_command(self._material_command)
        return self

    def move(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Object3D:
        if self.x != x or self.y != y or self.z != z:
            self.x = x
            self.y = y
            self.z = z
            self.run_command(self._move_command)
        return self

    def rotate(self, omega: float, phi: float, kappa: float):
        Rx = np.array([[1, 0, 0], [0, np.cos(omega), -np.sin(omega)], [0, np.sin(omega), np.cos(omega)]])
        Ry = np.array([[np.cos(phi), 0, np.sin(phi)], [0, 1, 0], [-np.sin(phi), 0, np.cos(phi)]])
        Rz = np.array([[np.cos(kappa), -np.sin(kappa), 0], [np.sin(kappa), np.cos(kappa), 0], [0, 0, 1]])
        return self.rotate_R((Rz @ Ry @ Rx).tolist())

    def rotate_R(self, R: List[List[float]]):
        if self.R != R:
            self.R = R
            self.run_command(self._rotate_command)
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
            self.run_command(self._scale_command)
        return self

    def visible(self, value: bool = True):
        if self.visible_ != value:
            self.visible_ = value
            self.run_command(self._visible_command)
        return self

    def delete(self):
        del self.view.objects[self.id]
        self.run_command(self._delete_command)
