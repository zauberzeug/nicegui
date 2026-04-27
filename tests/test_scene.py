import weakref
from typing import Literal

import numpy as np
import pytest
from selenium.common.exceptions import JavascriptException

from nicegui import app, ui
from nicegui.elements.scene import Object3D
from nicegui.testing import Screen, User

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


def _wait_for_scene_ready(screen: Screen, scene_id: int) -> None:
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return !!getElement({scene_id}) && !!getElement({scene_id}).renderer'
    ))


def _count_clipping_planes(screen: Screen, scene_id: int, object_id: str) -> int:
    return screen.selenium.execute_script(
        f'const o = getElement({scene_id}).objects.get("{object_id}");'
        'let n = 0;'
        'o.traverse((c) => {'
        '  if (!c.material) return;'
        '  const mats = Array.isArray(c.material) ? c.material : [c.material];'
        '  for (const m of mats) if (m.clippingPlanes) n += m.clippingPlanes.length;'
        '});'
        'return n;'
    )


def test_set_clipping_planes(screen: Screen):
    from nicegui import events
    scene = None
    box = None

    @ui.page('/')
    def page():
        nonlocal scene, box
        with ui.scene() as scene:
            box = scene.box()

    screen.open('/')
    _wait_for_scene_ready(screen, scene.id)
    box.set_clipping_planes([events.SceneClipPlane(nx=0, ny=0, nz=1, d=0)])
    screen.wait_for(lambda: _count_clipping_planes(screen, scene.id, box.id) >= 1)
    box.clear_clipping_planes()
    screen.wait_for(lambda: _count_clipping_planes(screen, scene.id, box.id) == 0)


async def test_clipping_planes_persisted_on_object_data(user: User):
    from nicegui import events
    box = None

    @ui.page('/')
    def page():
        nonlocal box
        with ui.scene() as scene:
            box = scene.box()

    await user.open('/')
    # The reload-survival contract: state set via set_clipping_planes lives on Object3D and is
    # part of its `data` tuple, which scene.js init_objects replays on every fresh connect.
    assert box.data[-1] == []
    box.set_clipping_planes([events.SceneClipPlane(nx=0, ny=0, nz=1, d=2)])
    assert box.data[-1] == [{'nx': 0, 'ny': 0, 'nz': 1, 'd': 2}]
    box.clear_clipping_planes()
    assert box.data[-1] == []


async def test_axes_inset_opts_cached_for_replay_on_init(user: User):
    # The reload-survival contract: state set via set_axes_inset/set_axes_labels is cached on
    # Scene and replayed in _handle_init, so a fresh client connect re-applies the inset.
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        scene = ui.scene()

    await user.open('/')
    assert scene._axes_inset_opts is None
    assert scene._axes_labels_opts is None
    scene.set_axes_inset(enabled=True, anchor='top-left', size=64, margin=8)
    assert scene._axes_inset_opts == {
        'enabled': True, 'size': 64, 'marginX': 8, 'marginY': 8, 'anchor': 'top-left',
    }
    scene.set_axes_labels(enabled=True, labels=('A', 'B', 'C'), color='#ff0000')
    assert scene._axes_labels_opts == {
        'enabled': True, 'labels': ['A', 'B', 'C'],
        'font': '24px Arial', 'color': '#ff0000', 'radius': 14,
    }


def test_set_axes_inset_and_labels(screen: Screen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        scene = ui.scene()

    screen.open('/')
    _wait_for_scene_ready(screen, scene.id)

    scene.set_axes_inset(enabled=True, size=64, anchor='top-left', margin=8)
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return !!getElement({scene.id}).viewHelper'
    ))

    # Labels and style are forwarded to viewHelper.setLabels / setLabelStyle. The cached opts
    # on the JS side are the most stable observable across three.js versions; deeper checks
    # against sprite material uuids are brittle.
    scene.set_axes_labels(enabled=True, labels=('Forward', 'Left', 'Up'),
                          font='20px sans-serif', color='#ff0000', radius=18)
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'const el = getElement({scene.id});'
        'return el.viewHelper && el._axesLabels && el._axesLabels.color === "#ff0000"'
    ))

    # Toggling enabled=False rebuilds a fresh ViewHelper on re-enable; the cached labels/style
    # must be reapplied so users don't lose their configuration.
    scene.set_axes_inset(enabled=False)
    screen.wait_for(lambda: not screen.selenium.execute_script(
        f'return !!getElement({scene.id}).viewHelper'
    ))
    scene.set_axes_inset(enabled=True, size=64, anchor='top-left', margin=8)
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'const el = getElement({scene.id});'
        'return !!el.viewHelper && el._axesLabels && el._axesLabels.color === "#ff0000"'
    ))


def test_axes_inset_handle_click_snaps_camera(screen: Screen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        scene = ui.scene()

    screen.open('/')
    _wait_for_scene_ready(screen, scene.id)
    scene.set_axes_inset(enabled=True)  # default anchor='bottom-right', size=128
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return !!getElement({scene.id}).viewHelper'
    ))

    # +X axis sprite is at world (1, 0, 0), which projects to inset NDC (0.5, 0) in the
    # orthoCamera's [-2, 2, -2, 2] frustum. Dispatch a pointerdown at that pixel and verify
    # viewHelper.animating flips on (then off when the snap-animation completes).
    animating = screen.selenium.execute_script(
        f'const el = getElement({scene.id});'
        'const canvas = el.renderer.domElement;'
        'const size = (el._axes && el._axes.size) || 128;'
        'const relX = (0.5 + 1) / 2 * size;'
        'const relY = (1 - 0) / 2 * size;'
        'const insetLeft = canvas.clientWidth - size;'
        'const insetTop = canvas.clientHeight - size;'
        'const rect = canvas.getBoundingClientRect();'
        'canvas.dispatchEvent(new PointerEvent("pointerdown", {'
        '  clientX: rect.left + insetLeft + relX,'
        '  clientY: rect.top + insetTop + relY,'
        '  bubbles: true, cancelable: true'
        '}));'
        'return el.viewHelper.animating;'
    )
    assert animating, 'Clicking the +X axis sprite should set viewHelper.animating = true'
    screen.wait_for(lambda: not screen.selenium.execute_script(
        f'return getElement({scene.id}).viewHelper.animating'
    ))


def test_intersection_planes_in_click_event(screen: Screen):
    from nicegui import events
    scene = None
    intersections: list = []

    @ui.page('/')
    def page():
        nonlocal scene

        def handle(e: events.SceneClickEventArguments):
            intersections.append(e.intersections)
        scene = ui.scene(
            on_click=handle,
            intersection_planes=[
                events.SceneIntersectionPlane(name='ground', axis='z', offset=0),
                events.SceneIntersectionPlane(name='wall', axis='x', offset=2),
            ],
        )

    screen.open('/')
    _wait_for_scene_ready(screen, scene.id)
    canvas = screen.find_by_tag('canvas')
    canvas.click()
    screen.wait_for(lambda: bool(intersections))
    keys = set(intersections[0].keys())
    assert keys == {'ground', 'wall'}


def test_raycaster_threshold_runtime_change(screen: Screen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        scene = ui.scene(raycaster_threshold=0.05)

    screen.open('/')
    _wait_for_scene_ready(screen, scene.id)
    assert screen.selenium.execute_script(
        f'return getElement({scene.id})._raycaster.params.Line.threshold'
    ) == 0.05
    scene._props['raycaster-threshold'] = 0.5
    scene.update()
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return getElement({scene.id})._raycaster.params.Line.threshold'
    ) == 0.5)
