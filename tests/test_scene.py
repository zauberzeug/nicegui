import gc
import weakref
from typing import Literal

import numpy as np
import pytest
from selenium.common.exceptions import JavascriptException
from selenium.webdriver import ActionChains

from nicegui import app, ui
from nicegui.elements.scene import Object3D
from nicegui.events import GenericEventArguments
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


def test_deleting_object_right_after_creation(screen: Screen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            scene.box().with_name('warmup')  # when the button is clicked, box.js is already loaded but group.js is not

        def create_and_delete():
            with scene, scene.group().with_name('group'):
                scene.box().with_name('box').delete()

        ui.button('Create and delete', on_click=create_and_delete)

    screen.open('/')
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("warmup")?.type', 'Mesh')
    screen.click('Create and delete')
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("group")?.type', 'Group')
    assert screen.selenium.execute_script(f'return scene_{scene.html_id}.getObjectByName("box")?.type ?? null') is None


def test_moving_right_after_detaching(screen: Screen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        scene = ui.scene()

        def detach_and_move():
            with scene, scene.group():
                box = scene.box().with_name('box')
            box.detach()
            box.move(1, 2, 3)

        ui.button('Detach and move', on_click=detach_and_move)

    screen.open('/')
    screen.click('Detach and move')
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("box")?.parent?.type', 'Scene')
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("box")?.position.x', 1)


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
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByProperty("object_id", "{obj.id}")?.children.length > 0', True)
    result = screen.selenium.execute_script(f'''
        const group = scene_{scene.html_id}.getObjectByProperty("object_id", "{obj.id}");
        const child = group.children[0];
        return {{
            root_type: group.type,
            child_geometry: child ? child.geometry.type : null,
            edge_count: (child && child.geometry.attributes.position) ? child.geometry.attributes.position.count : 0,
            child_color: (child && child.material) ? child.material.color.getHexString() : null,
        }};
    ''')
    assert result['root_type'] == 'Group', f'expected a Group wrapper, got {result}'
    assert result['child_geometry'] == 'EdgesGeometry', f'expected EdgesGeometry child, got {result}'
    assert result['edge_count'] > 0, f'expected non-empty edges, got {result}'
    assert result['child_color'] == 'ff0000', f'expected material to reach the wireframe lines, got {result}'

    screen.click('Rename')  # rename AFTER the async load has completed
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByProperty("object_id", "{obj.id}").name', 'renamed')


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


def test_moving_camera_keeps_controls_unless_up_vector_changes(screen: Screen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        scene = ui.scene()

    screen.open('/')
    screen.wait_for(lambda: scene is not None)
    enable_rotate = f'getElement({scene.id}).controls.enableRotate'
    screen.selenium.execute_script(f'{enable_rotate} = false')

    camera_x = f'getElement({scene.id}).camera.position.x'
    scene.move_camera(x=1, duration=0)
    screen.wait_for(lambda: screen.selenium.execute_script(f'return {camera_x}') == pytest.approx(1))
    assert screen.selenium.execute_script(f'return {enable_rotate}') is False, 'controls survive a plain camera move'

    camera_up_y = f'getElement({scene.id}).camera.up.y'
    scene.move_camera(up_y=1, up_z=0, duration=0)
    screen.wait_for(lambda: screen.selenium.execute_script(f'return {camera_up_y}') == pytest.approx(1))
    assert screen.selenium.execute_script(f'return {enable_rotate}') is True, 'controls are rebuilt for a new up vector'


def test_moving_camera_keeps_trackball_controls_after_rotating(screen: Screen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        scene = ui.scene(control_type='trackball')

    screen.open('/')
    screen.wait_for(lambda: scene is not None)
    static_moving = f'getElement({scene.id}).controls.staticMoving'
    screen.selenium.execute_script(f'{static_moving} = true')  # no rotation momentum after releasing the mouse

    canvas = screen.find_by_tag('canvas')
    screen.wait_for(canvas.is_displayed)  # the scene is hidden until it is initialized
    ActionChains(screen.selenium).click_and_hold(canvas).move_by_offset(50, 50).release().perform()
    camera_up_z = f'getElement({scene.id}).camera.up.z'
    screen.wait_for(lambda: screen.selenium.execute_script(f'return {camera_up_z}') != 1)  # the user rotated the scene

    camera_x = f'getElement({scene.id}).camera.position.x'
    scene.move_camera(x=1, duration=0)
    screen.wait_for(lambda: screen.selenium.execute_script(f'return {camera_x}') == pytest.approx(1))
    assert screen.selenium.execute_script(f'return {static_moving}') is True


def test_trackball_controls_follow_canvas_size(screen: Screen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        scene = ui.scene(control_type='trackball').classes('w-full h-64')

    screen.open('/')
    canvas = screen.find_by_tag('canvas')
    screen.wait_for(canvas.is_displayed)  # the scene is hidden until it is initialized
    assert canvas.size['width'] != 400, 'the canvas has been resized from its default size'
    screen_width = f'getElement({scene.id}).controls.screen.width'
    assert screen.selenium.execute_script(f'return {screen_width}') == canvas.size['width']


def test_configuring_controls_after_initialization(screen: Screen):
    scene = None

    @ui.page('/')
    async def page():
        nonlocal scene
        scene = ui.scene()
        scene.move_camera(up_y=1, up_z=0)
        await scene.initialized()
        ui.run_javascript(f'getElement({scene.id}).controls.enableRotate = false')

    screen.open('/')
    camera_up_y = f'getElement({scene.id}).camera.up.y'
    screen.wait_for(lambda: screen.selenium.execute_script(f'return {camera_up_y}') == pytest.approx(1))
    enable_rotate = f'getElement({scene.id}).controls.enableRotate'
    assert screen.selenium.execute_script(f'return {enable_rotate}') is False, 'configuration survives initialization'


async def test_dragend_after_object_deleted(user: User):
    events: list[str] = []
    scene = None
    box = None

    @ui.page('/')
    def page():
        nonlocal scene, box
        with ui.scene(on_drag_end=lambda e: events.append(e.object_id)) as scene:
            box = scene.box().draggable()

    await user.open('/')
    box.delete()
    assert box.id not in scene.objects
    scene._handle_drag(GenericEventArguments(sender=scene, client=scene.client, args={
        'type': 'dragend', 'object_id': box.id, 'object_name': None, 'x': 1.0, 'y': 2.0, 'z': 3.0,
    }))
    assert events == [box.id]


async def test_bound_object_is_released_on_delete(user: User):
    objects: weakref.WeakSet = weakref.WeakSet()

    @ui.page('/')
    def page():
        scene = ui.scene()
        label = ui.label()
        box = scene.box()
        objects.add(box)
        label.bind_text_from(box, 'x')
        box.delete()

    await user.open('/')
    gc.collect()
    assert len(objects) == 0


def test_context_loss_recovery_restores_objects(screen: Screen):
    scene = None

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            scene.box().material('#ff0000').move(1, 2, 3).with_name('box')

    screen.open('/')
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("box")?.position.x ?? null', 1)
    screen.selenium.execute_script(f'''
        window.sceneBeforeRecovery = scene_{scene.html_id};
        document.querySelector("canvas").getContext("webgl2").getExtension("WEBGL_lose_context").loseContext();
    ''')
    screen.click('Click to re-initialize')
    screen.wait_for_js(f'scene_{scene.html_id} !== window.sceneBeforeRecovery', True)  # remounting replaces the scene
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("box")?.position.x ?? null', 1)
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("box").material.color.getHexString()', 'ff0000')


def test_clicking_the_grid_reports_only_the_ground(screen: Screen):
    hits: list[str] = []

    @ui.page('/')
    def page():
        ui.scene(on_click=lambda e: hits.extend(hit.object_id for hit in e.hits))

    screen.open('/')
    screen.find_by_tag('canvas').click()
    screen.wait_for(lambda: hits == ['ground'])
