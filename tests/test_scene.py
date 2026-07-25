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


@pytest.mark.parametrize('set_material, color', [
    (False, 'e70000'),  # without material(), box.glb keeps its own red material (baseColorFactor 0.8 -> "e70000")
    (True, 'ff0000'),  # explicit material() overrides the model's own material
])
def test_gltf(screen: Screen, set_material: bool, color: str):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        app.add_static_file(local_file=TEST_DIR / 'media' / 'box.glb', url_path='/box.glb')
        with ui.scene() as scene:
            gltf = scene.gltf('/box.glb')
            if set_material:
                gltf.material(f'#{color}')

    screen.open('/')
    screen.wait(1.0)
    assert screen.selenium.execute_script(f'return scene_{scene.html_id}.children.length') == 5
    assert screen.selenium.execute_script(
        f'return scene_{scene.html_id}.children[4].getObjectByProperty("isMesh", true).material.color.getHexString()'
    ) == color


def test_stl_wireframe(screen: Screen):
    """A wireframe STL must render as edges (a LineSegments with EdgesGeometry), be colorable, and follow renames."""
    scene = None
    obj = None

    @ui.page('/')
    def page():
        nonlocal scene, obj
        app.add_static_file(local_file=TEST_DIR / 'media' / 'cube.stl', url_path='/cube.stl')
        with ui.scene() as scene:
            obj = scene.stl('/cube.stl', wireframe=True).material('#ff0000')
        ui.button('Rename', on_click=lambda: obj.with_name('renamed'))

    screen.open('/')
    screen.wait_for(lambda: obj is not None and screen.selenium.execute_script(
        f'return !!window.getElement && getElement({scene.id})?.objects?.get("{obj.id}")?.children.length > 0'
    ))
    result = screen.selenium.execute_script(f'''
        const obj = getElement({scene.id}).objects.get("{obj.id}");
        const child = obj.children && obj.children[0];
        return {{
            root_type: obj.type,
            child_geometry: child ? child.geometry.type : null,
            edge_count: (child && child.geometry.attributes.position) ? child.geometry.attributes.position.count : 0,
            child_object_id: child ? child.object_id : null,
            child_color: (child && child.material) ? child.material.color.getHexString() : null,
        }};
    ''')
    assert result['root_type'] == 'Group', f'expected a Group wrapper, got {result}'
    assert result['child_geometry'] == 'EdgesGeometry', f'expected EdgesGeometry child, got {result}'
    assert result['edge_count'] > 0, f'expected non-empty edges, got {result}'
    assert result['child_object_id'] == obj.id, f'expected click-hittable child with object_id, got {result}'
    assert result['child_color'] == 'ff0000', f'expected material to reach the wireframe lines, got {result}'

    screen.click('Rename')  # rename AFTER the async load has completed
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return getElement({scene.id}).objects.get("{obj.id}").children[0].name === "renamed"'
    ))


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
    scene.set_axes_inset(enabled=True, anchor='top-left', margin=8)
    assert scene._axes_inset_opts == {
        'enabled': True, 'marginX': 8, 'marginY': 8, 'anchor': 'top-left',
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

    scene.set_axes_inset(enabled=True, anchor='top-left', margin=8)
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return !!getElement({scene.id}).viewHelper'
    ))
    # location is what the r184 ViewHelper reads to position the inset; verify it matches.
    location = screen.selenium.execute_script(
        f'return getElement({scene.id}).viewHelper.location'
    )
    assert location == {'top': 8, 'bottom': None, 'left': 8, 'right': None}

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
    scene.set_axes_inset(enabled=True, anchor='top-left', margin=8)
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'const el = getElement({scene.id});'
        'return !!el.viewHelper && el._axesLabels && el._axesLabels.color === "#ff0000"'
    ))


def test_axes_inset_preserves_main_scene_render(screen: Screen):
    """``viewHelper.render()`` clears the framebuffer when ``renderer.autoClear`` is true,
    which wipes the main scene one draw after it renders. The render loop must save/restore
    ``autoClear`` around the helper call so the main scene survives each frame."""
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        scene = ui.scene()

    screen.open('/')
    _wait_for_scene_ready(screen, scene.id)
    scene.set_axes_inset(enabled=True)
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return !!getElement({scene.id}).viewHelper'
    ))
    # Patch viewHelper.render to record renderer.autoClear at call time. The render loop
    # must drop it to false before the helper draws — otherwise the helper wipes the main
    # scene's framebuffer.
    screen.selenium.execute_script(
        f'const el = getElement({scene.id});'
        'const orig = el.viewHelper.render.bind(el.viewHelper);'
        'window.__autoClearLog = [];'
        'el.viewHelper.render = function (renderer) {'
        '  window.__autoClearLog.push(renderer.autoClear);'
        '  return orig(renderer);'
        '};'
    )
    # Let the rAF loop run several frames.
    screen.wait(0.3)
    log = screen.selenium.execute_script('return window.__autoClearLog')
    assert len(log) >= 2, f'expected multiple viewHelper.render calls, got {log}'
    assert all(v is False for v in log), \
        f'renderer.autoClear must be false during viewHelper.render; got {log}'


def test_axes_inset_handle_click_snaps_camera(screen: Screen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        scene = ui.scene()

    screen.open('/')
    _wait_for_scene_ready(screen, scene.id)
    scene.set_axes_inset(enabled=True)  # default anchor='bottom-right', margin=0
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return !!getElement({scene.id}).viewHelper'
    ))

    # +X axis sprite is at world (1, 0, 0), which projects to inset NDC (0.5, 0) in the
    # orthoCamera's [-2, 2, -2, 2] frustum. Dispatch a pointerdown at that pixel and verify
    # viewHelper.animating flips on (then off when the snap-animation completes). Inset is
    # 128 px hardcoded inside three.js' ViewHelper; we use anchor=bottom-right, margin=0.
    animating = screen.selenium.execute_script(
        f'const el = getElement({scene.id});'
        'const canvas = el.renderer.domElement;'
        'const dim = 128;'
        'const relX = (0.5 + 1) / 2 * dim;'
        'const relY = (1 - 0) / 2 * dim;'
        'const insetLeft = canvas.clientWidth - dim;'
        'const insetTop = canvas.clientHeight - dim;'
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
