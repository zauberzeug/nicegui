import weakref

import numpy as np
from selenium.common.exceptions import JavascriptException

from nicegui import app, ui
from nicegui.elements.scene import Object3D
from nicegui.testing import SharedScreen

from .test_helpers import TEST_DIR


def test_moving_sphere_with_timer(shared_screen: SharedScreen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            sphere = scene.sphere().with_name('sphere')
            ui.timer(0.1, lambda: sphere.move(0, 0, sphere.z + 0.01))

    shared_screen.open('/')

    def position() -> float:
        for _ in range(3):
            try:
                pos = shared_screen.selenium.execute_script(
                    f'return scene_{scene.html_id}.getObjectByName("sphere").position.z')
                if pos is not None:
                    return pos
            except JavascriptException as e:
                print(e.msg, flush=True)
            shared_screen.wait(1.0)
        raise RuntimeError('Could not get position')

    shared_screen.wait(0.2)
    assert position() > 0


def test_no_object_duplication_on_index_client(shared_screen: SharedScreen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            sphere = scene.sphere().move(0, -4, 0)
            ui.timer(0.1, lambda: sphere.move(0, sphere.y + 0.5, 0))

    shared_screen.open('/')
    shared_screen.wait(0.4)
    shared_screen.switch_to(1)
    shared_screen.open('/')
    shared_screen.switch_to(0)
    shared_screen.wait(0.2)
    assert shared_screen.selenium.execute_script(f'return scene_{scene.html_id}.children.length') == 5


def test_no_object_duplication_with_page_builder(shared_screen: SharedScreen):
    scene_html_ids: list[int] = []

    @ui.page('/')
    def page():
        with ui.scene() as scene:
            sphere = scene.sphere().move(0, -4, 0)
            ui.timer(0.1, lambda: sphere.move(0, sphere.y + 0.5, 0))
        scene_html_ids.append(scene.html_id)

    shared_screen.open('/')
    shared_screen.wait(0.4)
    shared_screen.switch_to(1)
    shared_screen.open('/')
    shared_screen.switch_to(0)
    shared_screen.wait(0.2)
    assert shared_screen.selenium.execute_script(f'return scene_{scene_html_ids[0]}.children.length') == 5
    shared_screen.switch_to(1)
    shared_screen.wait(0.2)
    assert shared_screen.selenium.execute_script(f'return scene_{scene_html_ids[1]}.children.length') == 5


def test_deleting_group(shared_screen: SharedScreen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            with scene.group() as group:
                scene.sphere()
        ui.button('Delete group', on_click=group.delete)

    shared_screen.open('/')
    shared_screen.wait(0.5)
    assert len(scene.objects) == 2
    shared_screen.click('Delete group')
    shared_screen.wait(0.5)
    assert len(scene.objects) == 0


def test_replace_scene(shared_screen: SharedScreen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.row() as container:
            with ui.scene() as scene:
                scene.sphere().with_name('sphere')

        def replace():
            with container.clear():
                nonlocal scene
                with ui.scene() as scene:
                    scene.box().with_name('box')
        ui.button('Replace scene', on_click=replace)

    shared_screen.open('/')
    shared_screen.wait(0.5)
    assert shared_screen.selenium.execute_script(f'return scene_{scene.html_id}.children[4].name') == 'sphere'

    shared_screen.click('Replace scene')
    shared_screen.wait(0.5)
    assert shared_screen.selenium.execute_script(f'return scene_{scene.html_id}.children[4].name') == 'box'


def test_create_dynamically(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.button('Create', on_click=ui.scene)

    shared_screen.open('/')
    shared_screen.click('Create')
    assert shared_screen.find_by_tag('canvas')


def test_rotation_matrix_from_euler():
    omega, phi, kappa = 0.1, 0.2, 0.3
    Rx = np.array([[1, 0, 0], [0, np.cos(omega), -np.sin(omega)], [0, np.sin(omega), np.cos(omega)]])
    Ry = np.array([[np.cos(phi), 0, np.sin(phi)], [0, 1, 0], [-np.sin(phi), 0, np.cos(phi)]])
    Rz = np.array([[np.cos(kappa), -np.sin(kappa), 0], [np.sin(kappa), np.cos(kappa), 0], [0, 0, 1]])
    R = Rz @ Ry @ Rx
    assert np.allclose(Object3D.rotation_matrix_from_euler(omega, phi, kappa), R)


def test_object_creation_via_context(shared_screen: SharedScreen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            scene.box().with_name('box')

    shared_screen.open('/')
    shared_screen.wait(0.5)
    assert shared_screen.selenium.execute_script(f'return scene_{scene.html_id}.children[4].name') == 'box'


def test_object_creation_via_attribute(shared_screen: SharedScreen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        scene = ui.scene()
        scene.box().with_name('box')

    shared_screen.open('/')
    shared_screen.wait(0.5)
    assert shared_screen.selenium.execute_script(f'return scene_{scene.html_id}.children[4].name') == 'box'


def test_clearing_scene(shared_screen: SharedScreen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            scene.box().with_name('box')
            with scene.group():  # see https://github.com/zauberzeug/nicegui/issues/4560
                scene.box().with_name('box2')
        ui.button('Clear', on_click=scene.clear)

    shared_screen.open('/')
    shared_screen.wait(0.5)
    assert len(scene.objects) == 3
    shared_screen.click('Clear')
    shared_screen.wait(0.5)
    assert len(scene.objects) == 0


def test_gltf(shared_screen: SharedScreen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        app.add_static_file(local_file=TEST_DIR / 'media' / 'box.glb', url_path='/box.glb')
        with ui.scene() as scene:
            scene.gltf('/box.glb')

    shared_screen.open('/')
    shared_screen.wait(1.0)
    assert shared_screen.selenium.execute_script(f'return scene_{scene.html_id}.children.length') == 5


def test_no_cyclic_references(shared_screen: SharedScreen):
    objects: weakref.WeakSet = weakref.WeakSet()
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            for _ in range(10):
                objects.add(scene.box())

        ui.button('Clear', on_click=scene.clear)

    shared_screen.open('/')
    shared_screen.click('Clear')
    assert len(objects) == 0
