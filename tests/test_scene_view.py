import numpy as np

from nicegui import ui
from nicegui.testing import SharedScreen


def test_create_dynamically(shared_screen: SharedScreen):
    scene = scene_view = None

    @ui.page('/')
    def page():
        nonlocal scene
        scene = ui.scene()

        def create():
            nonlocal scene_view
            scene_view = ui.scene_view(scene)
        ui.button('Create', on_click=create)

    shared_screen.open('/')
    shared_screen.click('Create')
    shared_screen.wait(0.5)
    assert scene_view is not None
    assert shared_screen.selenium.execute_script(f'return getElement({scene_view.id}).scene == getElement({scene.id}).scene')


def test_object_creation_via_context(shared_screen: SharedScreen):
    scene = scene_view = None

    @ui.page('/')
    def page():
        nonlocal scene, scene_view
        with ui.scene() as scene:
            scene.box()

        scene_view = ui.scene_view(scene)

    shared_screen.open('/')
    shared_screen.wait(1)
    assert shared_screen.selenium.execute_script(f'return getElement({scene_view.id}).scene == getElement({scene.id}).scene')


def test_camera_move(shared_screen: SharedScreen):
    scene = scene_view = None

    @ui.page('/')
    def page():
        nonlocal scene, scene_view
        with ui.scene() as scene:
            scene.box()

        scene_view = ui.scene_view(scene)

    shared_screen.open('/')

    shared_screen.wait(0.5)
    scene_view.move_camera(x=1, y=2, z=3, look_at_x=4, look_at_y=5, look_at_z=6, up_x=7, up_y=8, up_z=9, duration=0.0)

    shared_screen.wait(1)
    position = shared_screen.selenium.execute_script(f'return getElement({scene_view.id}).camera_tween._object')
    assert np.allclose(position, [1, 2, 3, 7, 8, 9, 4, 5, 6])
