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


def test_polar_grid(screen: Screen):
    """Test that polar grid creates a scene with PolarGridHelper."""
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene(grid=False, polar_grid=(1.0, 8, 5)) as scene:
            scene.sphere(0.1).move(0.5, 0, 0)

    screen.open('/')
    screen.wait(0.5)
    # Scene should have: ambient light, directional light, ground (circle), polar grid, sphere = 5 children
    assert screen.selenium.execute_script(f'return scene_{scene.html_id}.children.length') == 5


def test_transform_controls_enable_disable(screen: Screen):
    """Test enabling and disabling TransformControls on an object."""
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            scene.box().with_name('box')

        def enable():
            scene.enable_transform_controls('box', mode='translate')

        def disable():
            scene.disable_transform_controls('box')

        ui.button('Enable', on_click=enable)
        ui.button('Disable', on_click=disable)

    screen.open('/')
    screen.wait(0.5)
    # Initially no transform controls
    initial_children = screen.selenium.execute_script(f'return scene_{scene.html_id}.children.length')

    screen.click('Enable')
    screen.wait(0.3)
    # TransformControls adds a helper to the scene
    after_enable = screen.selenium.execute_script(f'return scene_{scene.html_id}.children.length')
    assert after_enable > initial_children

    screen.click('Disable')
    screen.wait(0.3)
    # Helper should be removed
    after_disable = screen.selenium.execute_script(f'return scene_{scene.html_id}.children.length')
    assert after_disable == initial_children


def test_transform_controls_mode_change(screen: Screen):
    """Test changing TransformControls mode."""
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            scene.box().with_name('box')
        scene.enable_transform_controls('box', mode='translate')

        def set_rotate():
            scene.set_transform_mode('box', 'rotate')

        def set_scale():
            scene.set_transform_mode('box', 'scale')

        ui.button('Rotate', on_click=set_rotate)
        ui.button('Scale', on_click=set_scale)

    screen.open('/')
    screen.wait(0.5)
    # Just verify no errors are thrown when changing modes
    screen.click('Rotate')
    screen.wait(0.2)
    screen.click('Scale')
    screen.wait(0.2)
    # If we got here without errors, the test passes


def test_axes_inset(screen: Screen):
    """Test enabling and configuring the axes inset overlay."""
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            scene.sphere(0.5)

        def enable_inset():
            scene.set_axes_inset({'enabled': True, 'size': 80, 'anchor': 'bottom-left'})
            scene.set_axes_labels({'enabled': True})

        def disable_inset():
            scene.set_axes_inset({'enabled': False})

        ui.button('Enable Inset', on_click=enable_inset)
        ui.button('Disable Inset', on_click=disable_inset)

    screen.open('/')
    screen.wait(0.5)
    # Just verify no errors when toggling inset
    screen.click('Enable Inset')
    screen.wait(0.3)
    screen.click('Disable Inset')
    screen.wait(0.2)


def test_clipping_planes(screen: Screen):
    """Test setting and clearing clipping planes."""
    from nicegui.events import SceneClipPlane

    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            scene.sphere(0.5).with_name('sphere')

        def set_clip():
            # Clip below Z=0.1
            scene.set_clipping_planes('sphere', [SceneClipPlane(nx=0, ny=0, nz=1, d=-0.1)])

        def clear_clip():
            scene.clear_clipping_planes('sphere')

        ui.button('Set Clip', on_click=set_clip)
        ui.button('Clear Clip', on_click=clear_clip)

    screen.open('/')
    screen.wait(0.5)
    # Verify no errors when setting/clearing clipping planes
    screen.click('Set Clip')
    screen.wait(0.2)
    screen.click('Clear Clip')
    screen.wait(0.2)


def test_transform_controls_visible_axes(screen: Screen):
    """Test TransformControls with restricted visible axes."""
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            scene.box().with_name('box')

        def enable_z_only():
            scene.enable_transform_controls('box', mode='translate', visible_axes=['Z'])

        def enable_xy():
            scene.enable_transform_controls('box', mode='translate', visible_axes=['X', 'Y'])

        ui.button('Z Only', on_click=enable_z_only)
        ui.button('XY', on_click=enable_xy)

    screen.open('/')
    screen.wait(0.5)
    screen.click('Z Only')
    screen.wait(0.3)
    screen.click('XY')
    screen.wait(0.2)
    # If we got here without errors, axis restriction works


def test_ground_point_in_click_event(screen: Screen):
    """Test that click events include ground_point."""
    from nicegui import events

    ground_points: list = []

    @ui.page('/')
    def page():
        def on_click(e: events.SceneClickEventArguments):
            if e.ground_point:
                ground_points.append((e.ground_point.x, e.ground_point.y, e.ground_point.z))

        with ui.scene(on_click=on_click) as scene:
            scene.sphere(0.5).move(0, 0, 0.5)

    screen.open('/')
    screen.wait(0.5)
    # Click on the scene canvas
    canvas = screen.find_by_tag('canvas')
    canvas.click()
    screen.wait(0.3)
    # Ground point should be captured (Z should be 0 since it's ground plane intersection)
    assert len(ground_points) >= 1
    assert ground_points[0][2] == 0.0  # Z coordinate should be 0 for ground plane


def test_ground_plane_configurable(screen: Screen):
    """Test that ground_axis and ground_offset shift the ground-point intersection plane."""
    from nicegui import events

    ground_points: list = []

    @ui.page('/')
    def page():
        def on_click(e: events.SceneClickEventArguments):
            if e.ground_point:
                ground_points.append((e.ground_point.x, e.ground_point.y, e.ground_point.z))

        with ui.scene(on_click=on_click, ground_axis='z', ground_offset=0.5) as scene:
            scene.sphere(0.5).move(0, 0, 0.5)

    screen.open('/')
    screen.wait(0.5)
    canvas = screen.find_by_tag('canvas')
    canvas.click()
    screen.wait(0.3)
    assert len(ground_points) >= 1
    assert abs(ground_points[0][2] - 0.5) < 1e-6  # Z should land on the offset plane


def test_polyline(screen: Screen):
    """Test that polyline creates Line objects with the expected vertex count."""
    scene = None
    poly = None

    @ui.page('/')
    def page():
        nonlocal scene, poly
        with ui.scene(grid=False) as scene:
            poly = scene.polyline([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
            scene.polyline([[0, 0, 1], [1, 0, 1]], colors=[[1, 0, 0], [0, 1, 0]], dashed=True)

    screen.open('/')
    screen.wait(0.5)
    line_count = screen.selenium.execute_script(f'''
        let count = 0;
        scene_{scene.html_id}.traverse(o => {{ if (o.isLine) count++; }});
        return count;
    ''')
    assert line_count == 2
    vertex_count = screen.selenium.execute_script(
        f'return getElement({scene.id}).objects.get("{poly.id}").geometry.attributes.position.count'
    )
    assert vertex_count == 4


def test_lathe(screen: Screen):
    """Test that lathe creates a Mesh with LatheGeometry."""
    scene = None
    vase = None

    @ui.page('/')
    def page():
        nonlocal scene, vase
        with ui.scene(grid=False) as scene:
            vase = scene.lathe([[0, 0], [0.5, 0.2], [0.3, 0.5], [0, 0.8]], segments=8)

    screen.open('/')
    screen.wait(0.5)
    geometry_type = screen.selenium.execute_script(
        f'return getElement({scene.id}).objects.get("{vase.id}").geometry.type'
    )
    assert geometry_type == 'LatheGeometry'


def test_arrow_helper(screen: Screen):
    """Test that arrow_helper creates a Three.js ArrowHelper."""
    scene = None
    arrow = None

    @ui.page('/')
    def page():
        nonlocal scene, arrow
        with ui.scene(grid=False) as scene:
            arrow = scene.arrow_helper([0, 0, 1], origin=[0, 0, 0], length=1.5, color=0xff0000)

    screen.open('/')
    screen.wait(0.5)
    is_arrow = screen.selenium.execute_script(
        f'return getElement({scene.id}).objects.get("{arrow.id}").isArrowHelper === true'
    )
    assert is_arrow


def test_raycaster_threshold(screen: Screen):
    """Test that raycaster_threshold is forwarded to the Three.js raycaster."""
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        scene = ui.scene(raycaster_threshold=0.05)

    screen.open('/')
    screen.wait_for(lambda: scene is not None)
    screen.wait(0.3)
    threshold = screen.selenium.execute_script(
        f'return getElement({scene.id}).$props.raycasterThreshold'
    )
    assert threshold == 0.05


def test_hoverable(screen: Screen):
    """Test that marking an object as hoverable propagates the flag to the scene object."""
    scene = None
    box = None

    @ui.page('/')
    def page():
        nonlocal scene, box
        with ui.scene() as scene:
            box = scene.box().hoverable()

    screen.open('/')
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return !!(getElement({scene.id}) && getElement({scene.id}).objects && getElement({scene.id}).objects.get("{box.id}"))'
    ))
    is_hoverable = screen.selenium.execute_script(
        f'return getElement({scene.id}).objects.get("{box.id}")._hoverable === true'
    )
    assert is_hoverable


def test_set_orbit_enabled(screen: Screen):
    """Test that set_orbit_enabled toggles the OrbitControls `enabled` flag."""
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            scene.box()
        ui.button('Disable orbit', on_click=lambda: scene.set_orbit_enabled(False))
        ui.button('Enable orbit', on_click=lambda: scene.set_orbit_enabled(True))

    screen.open('/')
    screen.wait(0.5)
    screen.click('Disable orbit')
    screen.wait(0.2)
    assert screen.selenium.execute_script(f'return getElement({scene.id}).controls.enabled') is False
    screen.click('Enable orbit')
    screen.wait(0.2)
    assert screen.selenium.execute_script(f'return getElement({scene.id}).controls.enabled') is True
