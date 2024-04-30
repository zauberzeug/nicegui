from typing import Optional

from nicegui import ui
from nicegui.testing import Screen

import numpy as np

def test_create_dynamically(screen: Screen):
    scene = ui.scene()
    scene_view: Optional[ui.scene_view] = None

    def create():
        nonlocal scene_view
        scene_view = ui.scene_view(scene)
    ui.button('Create', on_click=create)

    screen.open('/')
    screen.click('Create')
    assert scene_view is not None
    assert screen.selenium.execute_script(f'return getElement({scene_view.id}).scene == getElement({scene.id})')


def test_object_creation_via_context(screen: Screen):
    with ui.scene() as scene:
        scene.box().with_name('box')

    scene_view = ui.scene_view(scene)

    screen.open('/')
    screen.wait(0.5)
    assert screen.selenium.execute_script(f'return getElement({scene_view.id}).scene == getElement({scene.id})')

def test_camera_move(screen: Screen):
    with ui.scene() as scene:
        scene.box().with_name('box')

    with ui.scene_view(scene) as scene_view:
        pass

    screen.open('/')

    screen.wait(0.5)
    scene_view.move_camera(x=1, y=2, z=3, look_at_x=4, look_at_y=5, look_at_z=6, up_x=7, up_y=8, up_z=9, duration=0.0)
    
    screen.wait(1)
    position = screen.selenium.execute_script(f'return getElement({scene_view.id}).camera_tween._object')
    assert np.allclose(position, [1, 2, 3, 7, 8, 9, 4, 5, 6])