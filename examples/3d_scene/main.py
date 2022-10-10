#!/usr/bin/env python3
import os

from nicegui import ui

ui.add_static_files('/static', f'{os.path.dirname(os.path.realpath(__file__))}/static')

with ui.scene(width=1024, height=800) as scene:
    scene.spot_light(distance=100, intensity=0.1).move(-10, 0, 10)
    scene.stl('static/pikachu.stl').scale(0.1)
    scene.move_camera(
        -5, -3, 3,  # position
        0, 0, 3,  # look at
        0, 0, 1,  # up
        0  # animation duration
    )

ui.run()
