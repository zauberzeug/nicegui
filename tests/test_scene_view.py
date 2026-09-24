import numpy as np

from nicegui import app, ui
from nicegui.testing import Screen

from .test_helpers import TEST_DIR


def test_create_dynamically(screen: Screen):
    scene = scene_view = None

    @ui.page('/')
    def page():
        nonlocal scene
        scene = ui.scene()

        def create():
            nonlocal scene_view
            scene_view = ui.scene_view(scene)
        ui.button('Create', on_click=create)

    screen.open('/')
    screen.click('Create')
    screen.wait(0.5)
    assert scene_view is not None
    assert screen.selenium.execute_script(f'return getElement({scene_view.id}).scene == getElement({scene.id}).scene')


def test_object_creation_via_context(screen: Screen):
    scene = scene_view = None

    @ui.page('/')
    def page():
        nonlocal scene, scene_view
        with ui.scene() as scene:
            scene.box()

        scene_view = ui.scene_view(scene)

    screen.open('/')
    screen.wait(1)
    assert screen.selenium.execute_script(f'return getElement({scene_view.id}).scene == getElement({scene.id}).scene')


def test_camera_move(screen: Screen):
    scene = scene_view = None

    @ui.page('/')
    def page():
        nonlocal scene, scene_view
        with ui.scene() as scene:
            scene.box()

        scene_view = ui.scene_view(scene)

    screen.open('/')

    screen.wait(0.5)
    scene_view.move_camera(x=1, y=2, z=3, look_at_x=4, look_at_y=5, look_at_z=6, up_x=7, up_y=8, up_z=9, duration=0.0)

    screen.wait(1)
    position = screen.selenium.execute_script(f'return getElement({scene_view.id}).camera_tween._object')
    assert np.allclose(position, [1, 2, 3, 7, 8, 9, 4, 5, 6])


def test_click_on_stl_with_untagged_children(screen: Screen):
    hits: list[str] = []
    scene = obj = None

    @ui.page('/')
    def page():
        nonlocal scene, obj
        app.add_static_file(local_file=TEST_DIR / 'media' / 'cube.stl', url_path='/cube.stl')
        with ui.scene(width=200, height=150) as scene:
            obj = scene.stl('/cube.stl').move(-0.5, -0.5, -0.5)  # center the cube in front of the camera

        ui.scene_view(scene, width=200, height=150, on_click=lambda e: hits.extend(hit.object_id for hit in e.hits))

    screen.open('/')
    query = f'scene_{scene.html_id}.getObjectByProperty("object_id", "{obj.id}")?.children.length > 0'
    screen.wait_for_js(query, True)  # the click must hit the child mesh created by the STL loader
    screen.find_all_by_tag('canvas')[1].click()
    screen.wait_for(lambda: obj.id in hits)
