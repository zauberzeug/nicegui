#!/usr/bin/env python3
"""Custom 3D scene-object example: a sphere that pulses via a Python-controlled scale."""

import math
import time

from typing_extensions import Self

from nicegui import ui
from nicegui.elements.scene.scene_object3d import Object3D


class PulsingSphere(Object3D, component='pulsing_sphere.js'):
    def __init__(self, radius: float = 1.0) -> None:
        super().__init__(radius)

    def set_scale(self, s: float) -> Self:
        self.run_method('set_scale', s)
        return self


with ui.scene(width=1024, height=800, fps=60) as scene:
    sphere = PulsingSphere(radius=1.0)

ui.timer(0.05, lambda: sphere.set_scale(1.0 + 0.4 * math.sin(time.time() * 3)))

ui.run()
