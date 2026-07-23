"""Behavioral tests for the per-object API of ui.scene.

Unlike test_scene.py, which mostly checks scene structure (child counts, names,
attach/detach), these tests pin the *observable Three.js state* produced by each
object type and method: geometry types, visibility, material color/opacity/side,
position/scale/rotation, texture and point cloud updates.

Assertions go through ``scene_<html_id>.getObjectByName(...)`` so they only
depend on the public scene graph, not on implementation details.
All state checks poll instead of sleeping, because object creation and method
dispatch may be asynchronous on the client.

Methods are exercised on a single representative object because they share one
central handler; only object creation differs per type and is covered for all types.
"""
import math

import numpy as np
import pytest
from selenium.common.exceptions import JavascriptException

from nicegui import app, ui
from nicegui.elements.scene import Object3D
from nicegui.testing import Screen

RED_PIXEL_PNG = ('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ'
                 'AAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==')
TRANSPARENT_PIXEL_PNG = ('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ'
                         'AAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=')

TEXTURE_COORDS_2X2: list[list[list[float] | None]] = [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
                                                      [[0.0, 1.0, 0.0], [1.0, 1.0, 0.0]]]
TEXTURE_COORDS_3X3: list[list[list[float] | None]] = [[[0.0, 0.0, 0.0], [0.5, 0.0, 0.0], [1.0, 0.0, 0.0]],
                                                      [[0.0, 0.5, 0.0], [0.5, 0.5, 0.0], [1.0, 0.5, 0.0]],
                                                      [[0.0, 1.0, 0.0], [0.5, 1.0, 0.0], [1.0, 1.0, 0.0]]]


def query(screen: Screen, scene: ui.scene, name: str, expression: str):
    """Evaluate a JS expression on the named object in the scene graph."""
    return screen.selenium.execute_script(
        f'const o = scene_{scene.html_id}.getObjectByName("{name}"); return o ? ({expression}) : null;')


def wait_until(screen: Screen, scene: ui.scene, name: str, expression: str, expected, *, timeout: float = 5.0):
    """Poll the JS expression on the named object until it equals the expected value."""
    value = None
    deadline = timeout
    while deadline > 0:
        try:
            value = query(screen, scene, name, expression)
            if value == expected:
                return
        except JavascriptException:
            pass
        screen.wait(0.1)
        deadline -= 0.1
    raise AssertionError(f'"{expression}" on "{name}" is {value!r}, expected {expected!r}')


def wait_for_object(screen: Screen, scene: ui.scene, name: str, *, timeout: float = 5.0):
    """Wait until the named object exists in the scene graph (creation may be asynchronous)."""
    wait_until(screen, scene, name, 'true', True, timeout=timeout)


def test_create_all_object_types(screen: Screen, tmp_path):
    stl_path = tmp_path / 'triangle.stl'
    stl_path.write_text('solid t\n'
                        'facet normal 0 0 1\n'
                        'outer loop\n'
                        'vertex 0 0 0\n'
                        'vertex 1 0 0\n'
                        'vertex 0 1 0\n'
                        'endloop\n'
                        'endfacet\n'
                        'endsolid t\n')
    scene: ui.scene = None  # type: ignore

    @ui.page('/')
    def page():
        nonlocal scene
        app.add_static_file(local_file=stl_path, url_path='/triangle.stl')
        with ui.scene() as scene:
            scene.box().with_name('box')
            scene.box(wireframe=True).with_name('box_wireframe')
            scene.sphere().with_name('sphere')
            scene.cylinder().with_name('cylinder')
            scene.ring().with_name('ring')
            scene.quadratic_bezier_tube([0, 0, 0], [0, 1, 0], [1, 1, 0]).with_name('tube')
            scene.extrusion([[0, 0], [0, 1], [1, 0.5]], 0.1).with_name('extrusion')
            scene.line([0, 0, 0], [1, 0, 0]).with_name('line')
            scene.curve([0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0]).with_name('curve')
            scene.texture(RED_PIXEL_PNG, TEXTURE_COORDS_2X2).with_name('texture')
            scene.spot_light().with_name('spot_light')
            scene.point_cloud([[0, 0, 0], [1, 1, 1]]).with_name('point_cloud')
            scene.group().with_name('group')
            scene.axes_helper().with_name('axes_helper')
            scene.text('2D').with_name('text')
            scene.text3d('3D').with_name('text3d')
            scene.stl('/triangle.stl').with_name('stl')

    screen.open('/')

    for name, expected_type, expected_geometry in [
        ('box', 'Mesh', 'BoxGeometry'),
        ('sphere', 'Mesh', 'SphereGeometry'),
        ('cylinder', 'Mesh', 'CylinderGeometry'),
        ('ring', 'Mesh', 'RingGeometry'),
        ('tube', 'Mesh', 'TubeGeometry'),
        ('extrusion', 'Mesh', 'ExtrudeGeometry'),
    ]:
        wait_for_object(screen, scene, name)
        assert query(screen, scene, name, 'o.type') == expected_type, f'{name} type'
        assert query(screen, scene, name, 'o.geometry.type') == expected_geometry, f'{name} geometry'

    for name, expected_type in [
        ('box_wireframe', 'LineSegments'),
        ('line', 'Line'),
        ('curve', 'Line'),
        ('texture', 'Mesh'),
        ('point_cloud', 'Points'),
        ('group', 'Group'),
        ('axes_helper', 'AxesHelper'),
    ]:
        wait_for_object(screen, scene, name)
        assert query(screen, scene, name, 'o.type') == expected_type, f'{name} type'

    wait_for_object(screen, scene, 'spot_light')
    assert query(screen, scene, 'spot_light', 'o.children.some(c => c.isSpotLight)') is True
    wait_for_object(screen, scene, 'text')
    assert query(screen, scene, 'text', 'o.isCSS2DObject') is True
    wait_for_object(screen, scene, 'text3d')
    assert query(screen, scene, 'text3d', 'o.isCSS3DObject') is True
    assert query(screen, scene, 'point_cloud', 'o.geometry.attributes.position.count') == 2
    wait_until(screen, scene, 'stl', 'o.children[0]?.geometry.attributes.position.count', 3)


def test_visible(screen: Screen):
    scene: ui.scene = None  # type: ignore
    box: Object3D = None  # type: ignore

    @ui.page('/')
    def page():
        nonlocal scene, box
        with ui.scene() as scene:
            box = scene.box().with_name('box')

    screen.open('/')
    wait_for_object(screen, scene, 'box')
    assert query(screen, scene, 'box', 'o.visible') is True
    box.visible(False)
    wait_until(screen, scene, 'box', 'o.visible', False)
    box.visible(True)
    wait_until(screen, scene, 'box', 'o.visible', True)


def test_material(screen: Screen):
    scene: ui.scene = None  # type: ignore
    box: Object3D = None  # type: ignore

    @ui.page('/')
    def page():
        nonlocal scene, box
        with ui.scene() as scene:
            box = scene.box().with_name('box')

    screen.open('/')
    wait_for_object(screen, scene, 'box')

    box.material('#00ff00', opacity=0.5, side='both')
    wait_until(screen, scene, 'box', 'o.material.color.getHexString()', '00ff00')
    assert query(screen, scene, 'box', 'o.material.opacity') == 0.5
    assert query(screen, scene, 'box', 'o.material.side') == 2  # THREE.DoubleSide


def test_move_scale_rotate(screen: Screen):
    scene: ui.scene = None  # type: ignore
    box: Object3D = None  # type: ignore

    @ui.page('/')
    def page():
        nonlocal scene, box
        with ui.scene() as scene:
            box = scene.box().with_name('box')

    screen.open('/')
    wait_for_object(screen, scene, 'box')

    box.move(1, 2, 3)
    box.scale(2, 3, 4)
    box.rotate(0.1, 0.2, 0.3)
    wait_until(screen, scene, 'box', 'o.position.toArray()', [1, 2, 3])
    wait_until(screen, scene, 'box', 'o.scale.toArray()', [2, 3, 4])
    R = np.array(Object3D.rotation_matrix_from_euler(0.1, 0.2, 0.3))
    expected = [math.atan2(-R[1, 2], R[2, 2]), math.asin(R[0, 2]), math.atan2(-R[0, 1], R[0, 0])]  # XYZ euler order
    wait_until(screen, scene, 'box', 'o.rotation.x !== 0', True)
    rotation = query(screen, scene, 'box', 'o.rotation.toArray()')
    assert rotation[:3] == pytest.approx(expected, abs=1e-6)


def test_attach_and_detach(screen: Screen):
    scene: ui.scene = None  # type: ignore
    box: Object3D = None  # type: ignore
    group: Object3D = None  # type: ignore

    @ui.page('/')
    def page():
        nonlocal scene, box, group
        with ui.scene() as scene:
            group = scene.group().with_name('group').move(1, 0, 0)
            box = scene.box().with_name('box')

    screen.open('/')
    wait_for_object(screen, scene, 'group')
    wait_for_object(screen, scene, 'box')
    assert query(screen, scene, 'box', 'o.parent.type') == 'Scene'

    box.attach(group)
    wait_until(screen, scene, 'box', 'o.parent.name', 'group')
    wait_until(screen, scene, 'box', 'o.position.toArray()', [-1, 0, 0])  # position in space is preserved

    box.detach()
    wait_until(screen, scene, 'box', 'o.parent.type', 'Scene')
    wait_until(screen, scene, 'box', 'o.position.toArray()', [0, 0, 0])


def test_texture_set_url_and_coordinates(screen: Screen):
    scene: ui.scene = None  # type: ignore
    texture = None

    @ui.page('/')
    def page():
        nonlocal scene, texture
        with ui.scene() as scene:
            texture = scene.texture(RED_PIXEL_PNG, TEXTURE_COORDS_2X2).with_name('texture')

    screen.open('/')
    wait_for_object(screen, scene, 'texture')
    assert query(screen, scene, 'texture', 'o.geometry.attributes.position.count') == 4

    texture.set_coordinates(TEXTURE_COORDS_3X3)
    wait_until(screen, scene, 'texture', 'o.geometry.attributes.position.count', 9)

    texture.set_url(TRANSPARENT_PIXEL_PNG)
    wait_until(screen, scene, 'texture', 'o.material.map.image?.src', TRANSPARENT_PIXEL_PNG)

    texture.set_url(RED_PIXEL_PNG)  # a second update must work as well
    wait_until(screen, scene, 'texture', 'o.material.map.image?.src', RED_PIXEL_PNG)


def test_point_cloud_set_points(screen: Screen):
    scene: ui.scene = None  # type: ignore
    point_cloud = None

    @ui.page('/')
    def page():
        nonlocal scene, point_cloud
        with ui.scene() as scene:
            point_cloud = scene.point_cloud([[0, 0, 0], [1, 1, 1]]).with_name('point_cloud')

    screen.open('/')
    wait_for_object(screen, scene, 'point_cloud')
    assert query(screen, scene, 'point_cloud', 'o.geometry.attributes.position.count') == 2

    point_cloud.set_points([[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3]], [[1, 0, 0]] * 4)
    wait_until(screen, scene, 'point_cloud', 'o.geometry.attributes.position.count', 4)
    assert query(screen, scene, 'point_cloud', 'o.geometry.attributes.color.count') == 4
