import numpy as np
from selenium.common.exceptions import JavascriptException

from nicegui import ui
from nicegui.elements.scene_object3d import Object3D
from nicegui.testing import Screen


def test_moving_sphere_with_timer(screen: Screen):
    with ui.scene() as scene:
        sphere = scene.sphere().with_name('sphere')
        ui.timer(0.1, lambda: sphere.move(0, 0, sphere.z + 0.01))

    screen.open('/')

    def position() -> float:
        for _ in range(3):
            try:
                pos = screen.selenium.execute_script(f'return scene_c{scene.id}.getObjectByName("sphere").position.z')
                if pos is not None:
                    return pos
            except JavascriptException as e:
                print(e.msg, flush=True)
            screen.wait(1.0)
        raise RuntimeError('Could not get position')

    screen.wait(0.2)
    assert position() > 0


def test_no_object_duplication_on_index_client(screen: Screen):
    with ui.scene() as scene:
        sphere = scene.sphere().move(0, -4, 0)
        ui.timer(0.1, lambda: sphere.move(0, sphere.y + 0.5, 0))

    screen.open('/')
    screen.wait(0.4)
    screen.switch_to(1)
    screen.open('/')
    screen.switch_to(0)
    screen.wait(0.2)
    assert screen.selenium.execute_script(f'return scene_c{scene.id}.children.length') == 5


def test_no_object_duplication_with_page_builder(screen: Screen):
    scene: ui.scene

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            sphere = scene.sphere().move(0, -4, 0)
            ui.timer(0.1, lambda: sphere.move(0, sphere.y + 0.5, 0))

    screen.open('/')
    screen.wait(0.4)
    screen.switch_to(1)
    screen.open('/')
    screen.switch_to(0)
    screen.wait(0.2)
    assert screen.selenium.execute_script(f'return scene_c{scene.id}.children.length') == 5
    screen.switch_to(1)
    assert screen.selenium.execute_script(f'return scene_c{scene.id}.children.length') == 5


def test_deleting_group(screen: Screen):
    with ui.scene() as scene:
        with scene.group() as group:
            scene.sphere()
    ui.button('Delete group', on_click=group.delete)

    screen.open('/')
    screen.wait(0.5)
    assert len(scene.objects) == 2
    screen.click('Delete group')
    screen.wait(0.5)
    assert len(scene.objects) == 0


def test_replace_scene(screen: Screen):
    with ui.row() as container:
        with ui.scene() as scene:
            scene.sphere().with_name('sphere')

    def replace():
        container.clear()
        with container:
            nonlocal scene
            with ui.scene() as scene:
                scene.box().with_name('box')
    ui.button('Replace scene', on_click=replace)

    screen.open('/')
    screen.wait(0.5)
    assert screen.selenium.execute_script(f'return scene_c{scene.id}.children[4].name') == 'sphere'
    screen.click('Replace scene')
    screen.wait(0.5)
    assert screen.selenium.execute_script(f'return scene_c{scene.id}.children[4].name') == 'box'


def test_create_dynamically(screen: Screen):
    ui.button('Create', on_click=ui.scene)

    screen.open('/')
    screen.click('Create')
    assert screen.find_by_tag('canvas')


def test_rotation_matrix_from_euler():
    omega, phi, kappa = 0.1, 0.2, 0.3
    Rx = np.array([[1, 0, 0], [0, np.cos(omega), -np.sin(omega)], [0, np.sin(omega), np.cos(omega)]])
    Ry = np.array([[np.cos(phi), 0, np.sin(phi)], [0, 1, 0], [-np.sin(phi), 0, np.cos(phi)]])
    Rz = np.array([[np.cos(kappa), -np.sin(kappa), 0], [np.sin(kappa), np.cos(kappa), 0], [0, 0, 1]])
    R = Rz @ Ry @ Rx
    assert np.allclose(Object3D.rotation_matrix_from_euler(omega, phi, kappa), R)


def test_object_creation_via_context(screen: Screen):
    with ui.scene() as scene:
        scene.box().with_name('box')

    screen.open('/')
    screen.wait(0.5)
    assert screen.selenium.execute_script(f'return scene_c{scene.id}.children[4].name') == 'box'


def test_object_creation_via_attribute(screen: Screen):
    scene = ui.scene()
    scene.box().with_name('box')

    screen.open('/')
    screen.wait(0.5)
    assert screen.selenium.execute_script(f'return scene_c{scene.id}.children[4].name') == 'box'


def test_clearing_scene(screen: Screen):
    with ui.scene() as scene:
        scene.box().with_name('box')
        scene.box().with_name('box2')
    ui.button('Clear', on_click=scene.clear)

    screen.open('/')
    screen.wait(0.5)
    assert len(scene.objects) == 2
    screen.click('Clear')
    screen.wait(0.5)
    assert len(scene.objects) == 0


def test_gltf(screen: Screen):
    with ui.scene() as scene:
        scene.gltf('https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models/Box/glTF-Binary/Box.glb')

    screen.open('/')
    screen.wait(1.0)
    assert screen.selenium.execute_script(f'return scene_c{scene.id}.children.length') == 5
