#!/usr/bin/env python3
"""Custom 3D scene-object example: a road extruded along a curve with direction indicators."""

from itertools import cycle

from typing_extensions import Self

from nicegui import ui
from nicegui.elements.scene.scene_object3d import Object3D


class DynamicRoad(Object3D, component='dynamic_road.js'):
    def __init__(self, curves: list[dict], width: float, thickness: float) -> None:
        super().__init__(curves, width, thickness)

    def set_curves(self, curves: list[dict]) -> Self:
        self.run_method('set_curves', curves)
        return self

    def set_arrow_color(self, color: str) -> Self:
        self.run_method('set_arrow_color', color)
        return self


curves_a = [
    {'type': 'cubic', 'v0': [0, 0, 0], 'v1': [1, 2, 0], 'v2': [3, 2, 0], 'v3': [4, 0, 0]},
    {'type': 'line', 'v0': [4, 0, 0], 'v1': [6, 0, 0]},
]

curves_b = [
    {'type': 'catmullrom', 'points': [[0, 0, 0], [1, 1, 0.5], [2, 0, 0.7], [3, -1, 0.5], [4, 0, 0]]},
]

with ui.scene(width=1024, height=800, fps=60) as scene:
    road = DynamicRoad(curves=curves_a, width=0.5, thickness=0.1).material('#808080')

color_iterator = cycle(['#ff00ff', '#0099ee'])
curve_iterator = cycle([curves_b, curves_a])
ui.button('Change color', on_click=lambda: road.set_arrow_color(next(color_iterator)))
ui.button('Swap curves', on_click=lambda: road.set_curves(next(curve_iterator)))

ui.run()
