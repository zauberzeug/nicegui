import weakref
from typing import Literal

import numpy as np
import pytest
from selenium.common.exceptions import JavascriptException

from nicegui import app, ui
from nicegui.elements.scene import Object3D
from nicegui.testing import Screen

from .test_helpers import TEST_DIR


def test_moving_sphere_with_timer(screen: Screen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            sphere = scene.sphere().with_name('sphere')
            ui.timer(0.1, lambda: sphere.move(0, 0, sphere.z + 0.01))

    screen.open('/')

    def position() -> float:
        for _ in range(3):
            try:
                pos = screen.selenium.execute_script(
                    f'return scene_{scene.html_id}.getObjectByName("sphere").position.z')
                if pos is not None:
                    return pos
            except JavascriptException as e:
                print(e.msg, flush=True)
            screen.wait(1.0)
        raise RuntimeError('Could not get position')

    screen.wait(0.2)
    assert position() > 0


def test_no_object_duplication_on_index_client(screen: Screen):
    scene = None

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
    assert screen.selenium.execute_script(f'return scene_{scene.html_id}.children.length') == 5


def test_no_object_duplication_with_page_builder(screen: Screen):
    scene_html_ids: list[int] = []

    @ui.page('/')
    def page():
        with ui.scene() as scene:
            sphere = scene.sphere().move(0, -4, 0)
            ui.timer(0.1, lambda: sphere.move(0, sphere.y + 0.5, 0))
        scene_html_ids.append(scene.html_id)

    screen.open('/')
    screen.wait(0.4)
    screen.switch_to(1)
    screen.open('/')
    screen.switch_to(0)
    screen.wait(0.2)
    assert screen.selenium.execute_script(f'return scene_{scene_html_ids[0]}.children.length') == 5
    screen.switch_to(1)
    screen.wait(0.2)
    assert screen.selenium.execute_script(f'return scene_{scene_html_ids[1]}.children.length') == 5


def test_deleting_group(screen: Screen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
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

    screen.open('/')
    screen.wait(0.5)
    assert screen.selenium.execute_script(f'return scene_{scene.html_id}.children[4].name') == 'sphere'

    screen.click('Replace scene')
    screen.wait(0.5)
    assert screen.selenium.execute_script(f'return scene_{scene.html_id}.children[4].name') == 'box'


def test_create_dynamically(screen: Screen):
    @ui.page('/')
    def page():
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


def test_rotation_matrix_from_euler_all_orders():
    rx, ry, rz = 0.4, -0.3, 0.5
    Rx = np.array([[1, 0, 0], [0, np.cos(rx), -np.sin(rx)], [0, np.sin(rx), np.cos(rx)]])
    Ry = np.array([[np.cos(ry), 0, np.sin(ry)], [0, 1, 0], [-np.sin(ry), 0, np.cos(ry)]])
    Rz = np.array([[np.cos(rz), -np.sin(rz), 0], [np.sin(rz), np.cos(rz), 0], [0, 0, 1]])
    axis = {'X': Rx, 'Y': Ry, 'Z': Rz}
    for order in Object3D.EULER_ORDERS:
        # Intrinsic order: rightmost axis is applied first to the body, so order='YXZ' → Rz @ Rx @ Ry.
        expected = axis[order[2]] @ axis[order[1]] @ axis[order[0]]
        actual = Object3D.rotation_matrix_from_euler(rx, ry, rz, order)
        assert np.allclose(actual, expected), f'{order} mismatch:\n{actual}\nvs\n{expected}'


def test_rotation_matrix_from_euler_rejects_bad_order():
    import pytest as _pytest
    with _pytest.raises(ValueError, match='Unsupported Euler order'):
        Object3D.rotation_matrix_from_euler(0, 0, 0, 'XYY')  # type: ignore[arg-type]


def test_object_creation_via_context(screen: Screen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            scene.box().with_name('box')

    screen.open('/')
    screen.wait(0.5)
    assert screen.selenium.execute_script(f'return scene_{scene.html_id}.children[4].name') == 'box'


def test_object_creation_via_attribute(screen: Screen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        scene = ui.scene()
        scene.box().with_name('box')

    screen.open('/')
    screen.wait(0.5)
    assert screen.selenium.execute_script(f'return scene_{scene.html_id}.children[4].name') == 'box'


def test_clearing_scene(screen: Screen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            scene.box().with_name('box')
            with scene.group():  # see https://github.com/zauberzeug/nicegui/issues/4560
                scene.box().with_name('box2')
        ui.button('Clear', on_click=scene.clear)

    screen.open('/')
    screen.wait(0.5)
    assert len(scene.objects) == 3
    screen.click('Clear')
    screen.wait(0.5)
    assert len(scene.objects) == 0


def test_gltf(screen: Screen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        app.add_static_file(local_file=TEST_DIR / 'media' / 'box.glb', url_path='/box.glb')
        with ui.scene() as scene:
            scene.gltf('/box.glb')

    screen.open('/')
    screen.wait(1.0)
    assert screen.selenium.execute_script(f'return scene_{scene.html_id}.children.length') == 5


def test_no_cyclic_references(screen: Screen):
    objects: weakref.WeakSet = weakref.WeakSet()
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            for _ in range(10):
                objects.add(scene.box())

        ui.button('Clear', on_click=scene.clear)

    screen.open('/')
    screen.click('Clear')
    assert len(objects) == 0


@pytest.mark.parametrize('control_type,constructor', [('map', 'MapControls'), ('trackball', 'TrackballControls')])
def test_custom_controls(screen: Screen, control_type: Literal['map', 'trackball'], constructor: str):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        scene = ui.scene(control_type=control_type)

    screen.open('/')
    screen.wait_for(lambda: scene is not None)
    assert screen.selenium.execute_script(f'return getElement({scene.id}).controls.constructor.name') == constructor


def test_polyline(screen: Screen):
    scene = None
    line_obj = None

    @ui.page('/')
    def page():
        nonlocal scene, line_obj
        with ui.scene() as scene:
            line_obj = scene.polyline(
                points=[[0, 0, 0], [1, 0, 0], [1, 1, 0]],
                colors=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                dashed=True,
                dash_size=0.1,
                gap_size=0.05,
            )

    screen.open('/')
    screen.wait(0.5)
    is_line = screen.selenium.execute_script(
        f'const o = getElement({scene.id}).objects.get("{line_obj.id}");'
        'return o.isLine === true && o.material.type === "LineDashedMaterial" && o.material.vertexColors === true;'
    )
    assert is_line


def test_lathe(screen: Screen):
    scene = None
    obj = None

    @ui.page('/')
    def page():
        nonlocal scene, obj
        with ui.scene() as scene:
            obj = scene.lathe(points=[[0, 0], [0.5, 0.5], [0, 1]], segments=8)

    screen.open('/')
    screen.wait(0.5)
    is_lathe = screen.selenium.execute_script(
        f'const o = getElement({scene.id}).objects.get("{obj.id}");'
        'return o.isMesh === true && o.geometry.type === "LatheGeometry";'
    )
    assert is_lathe


def test_arrow_helper(screen: Screen):
    scene = None
    arrow = None

    @ui.page('/')
    def page():
        nonlocal scene, arrow
        with ui.scene() as scene:
            arrow = scene.arrow_helper(direction=[0, 0, 1], origin=[0, 0, 0], length=1.0,
                                       color=0xff0000, radial_segments=24)

    screen.open('/')
    screen.wait(0.5)
    is_arrow = screen.selenium.execute_script(
        f'const o = getElement({scene.id}).objects.get("{arrow.id}");'
        'return o.type === "ArrowHelper" && o.cone.geometry.parameters.radialSegments === 24;'
    )
    assert is_arrow


def test_polar_grid_helper(screen: Screen):
    scene = None
    grid = None

    @ui.page('/')
    def page():
        nonlocal scene, grid
        with ui.scene() as scene:
            grid = scene.polar_grid_helper(radius=5.0, sectors=8, rings=4)

    screen.open('/')
    screen.wait(0.5)
    is_grid = screen.selenium.execute_script(
        f'const o = getElement({scene.id}).objects.get("{grid.id}");'
        'return o.type === "PolarGridHelper";'
    )
    assert is_grid


def test_rotate_with_order(screen: Screen):
    scene = None
    box = None

    @ui.page('/')
    def page():
        nonlocal scene, box
        with ui.scene() as scene:
            box = scene.box().rotate(0.4, -0.3, 0.5, order='ZYX')

    screen.open('/')
    screen.wait(0.5)
    expected = Object3D.rotation_matrix_from_euler(0.4, -0.3, 0.5, 'ZYX')
    assert np.allclose(box.R, expected)
    # Verify the rotation persists through a re-send to the client.
    server_R = screen.selenium.execute_script(
        f'const o = getElement({scene.id}).objects.get("{box.id}");'
        'const m = o.matrixWorld.elements;'
        # Three.js stores column-major; pull out the upper-left 3x3.
        'return [[m[0], m[4], m[8]], [m[1], m[5], m[9]], [m[2], m[6], m[10]]];'
    )
    assert np.allclose(server_R, expected, atol=1e-6)
