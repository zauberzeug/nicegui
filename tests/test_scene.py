import gc
import weakref
from typing import Literal

import numpy as np
import pytest
from selenium.common.exceptions import JavascriptException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder

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


def test_transform_controls_enable_disable(screen: Screen):
    scene = None
    box = None

    @ui.page('/')
    def page():
        nonlocal scene, box
        with ui.scene() as scene:
            box = scene.box()
        ui.button('Enable', on_click=lambda: box.enable_transform_controls(mode='translate'))
        ui.button('Disable', on_click=box.disable_transform_controls)

    screen.open('/')
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'const el = getElement({scene.id}); return el && !!el.renderer'
    ))
    screen.click('Enable')
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return getElement({scene.id}).has_transform_controls("{box.id}")'
    ))
    screen.click('Disable')
    screen.wait_for(lambda: not screen.selenium.execute_script(
        f'return getElement({scene.id}).has_transform_controls("{box.id}")'
    ))


def test_transform_controls_mode_change(screen: Screen):
    scene = None
    box = None

    @ui.page('/')
    def page():
        nonlocal scene, box
        with ui.scene() as scene:
            box = scene.box()
        ui.button('Translate', on_click=lambda: box.enable_transform_controls(mode='translate'))
        ui.button('Rotate', on_click=lambda: box.set_transform_mode('rotate'))
        ui.button('Scale', on_click=lambda: box.set_transform_mode('scale'))

    screen.open('/')
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'const el = getElement({scene.id}); return el && !!el.renderer'
    ))
    screen.click('Translate')
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return getElement({scene.id}).transform_controls.get("{box.id}")?.mode === "translate"'
    ))
    screen.click('Rotate')
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return getElement({scene.id}).transform_controls.get("{box.id}")?.mode === "rotate"'
    ))
    screen.click('Scale')
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return getElement({scene.id}).transform_controls.get("{box.id}")?.mode === "scale"'
    ))


def test_set_orbit_enabled_survives_transform_drag(screen: Screen):
    """Locks in the regression for the orbit drag-counter race: a TransformControls drag-end must
    not silently re-enable OrbitControls if the user has explicitly disabled them."""
    scene = None
    box = None

    @ui.page('/')
    def page():
        nonlocal scene, box
        scene = ui.scene()
        with scene:
            box = scene.box()
        ui.button('Disable orbit', on_click=lambda: scene.set_orbit_enabled(False))
        ui.button('Enable transform', on_click=lambda: box.enable_transform_controls(mode='translate'))

    screen.open('/')
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'const el = getElement({scene.id}); return el && !!el.renderer'
    ))
    screen.click('Disable orbit')
    screen.wait_for(lambda: not screen.selenium.execute_script(
        f'return getElement({scene.id}).controls.enabled'
    ))
    screen.click('Enable transform')
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return getElement({scene.id}).has_transform_controls("{box.id}")'
    ))
    # Simulate a TransformControls drag start + end via JS, mimicking what the gizmo does on
    # mouse-down + mouse-up. The fix under test ensures controls.enabled stays false afterward.
    screen.selenium.execute_script(
        f'const el = getElement({scene.id});'
        f'const tc = el.transform_controls.get("{box.id}");'
        'tc.dispatchEvent({type: "dragging-changed", value: true});'
        'tc.dispatchEvent({type: "dragging-changed", value: false});'
    )
    assert screen.selenium.execute_script(
        f'return getElement({scene.id}).controls.enabled'
    ) is False


def test_interactive_state_survives_context_loss(screen: Screen):
    """_resend() replays handler registrations and hover effects when the scene remounts."""
    scene = None
    box = None

    @ui.page('/')
    def page():
        nonlocal scene, box
        with ui.scene() as scene:
            box = scene.box().on_pointer_over(lambda _: None).hover_effect('glow', color='#ff0000')

    screen.open('/')
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'const el = getElement({scene.id}); return el && !!el.renderer'
    ))
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'const el = getElement({scene.id});'
        f'return el.objectHandlers.has("{box.id}") && el.objectEffects.has("{box.id}")'
    ))
    screen.selenium.execute_script(
        'document.querySelector("canvas").getContext("webgl2").getExtension("WEBGL_lose_context").loseContext();'
    )
    screen.click('Click to re-initialize')
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'const el = getElement({scene.id});'
        'if (!el || !el.objectHandlers) return false;'
        f'return el.objectHandlers.has("{box.id}") && el.objectEffects.has("{box.id}")'
    ))


def test_interactive_list_maintained_on_handler_register(screen: Screen):
    """Registering a handler from Python adds the underlying three.js object to the JS interactiveObjects list."""
    scene = None
    box = None

    @ui.page('/')
    def page():
        nonlocal scene, box
        with ui.scene() as scene:
            box = scene.box()
        ui.button('Add handler', on_click=lambda: box.on_pointer_over(lambda _: None))
        ui.button('Add effect', on_click=lambda: box.hover_effect('outline'))

    screen.open('/')
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'const el = getElement({scene.id}); return el && !!el.renderer'
    ))
    # Initially neither handlers nor effect set, so not interactive.
    assert screen.selenium.execute_script(
        f'return getElement({scene.id}).is_interactive("{box.id}")'
    ) is False
    screen.click('Add handler')
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return getElement({scene.id}).has_handler("{box.id}", "pointerover")'
    ))
    assert screen.selenium.execute_script(
        f'return getElement({scene.id}).interactiveObjects.length'
    ) == 1
    screen.click('Add effect')
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return getElement({scene.id}).has_effect("{box.id}")'
    ))
    # Adding an effect to an already-interactive object doesn't double-add it.
    assert screen.selenium.execute_script(
        f'return getElement({scene.id}).interactiveObjects.length'
    ) == 1


def test_hover_effect_named_variants(screen: Screen):
    """Each named effect installs the right kind of three.js artifact when hovered, and tears down cleanly."""
    scene = None
    box = None

    @ui.page('/')
    def page():
        nonlocal scene, box
        with ui.scene() as scene:
            box = scene.box()
        ui.button('Glow', on_click=lambda: box.hover_effect('glow'))
        ui.button('Outline', on_click=lambda: box.hover_effect('outline'))
        ui.button('Tint', on_click=lambda: box.hover_effect('tint', color='#ff0000'))
        ui.button('Off', on_click=lambda: box.hover_effect(False))

    screen.open('/')
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'const el = getElement({scene.id}); return el && !!el.renderer'
    ))

    def get_effect_spec() -> dict | None:
        return screen.selenium.execute_script(
            f'return getElement({scene.id}).objectEffects.get("{box.id}") ?? null'
        )

    screen.click('Glow')
    screen.wait_for(lambda: get_effect_spec() == {'effect': 'glow', 'color': None})

    screen.click('Outline')
    screen.wait_for(lambda: get_effect_spec() == {'effect': 'outline', 'color': None})

    screen.click('Tint')
    screen.wait_for(lambda: get_effect_spec() == {'effect': 'tint', 'color': '#ff0000'})

    screen.click('Off')
    screen.wait_for(lambda: get_effect_spec() is None)


def test_pointer_event_dispatches_to_object_handler(screen: Screen):
    """Synthesizing a JS-side pointerevent should invoke the registered per-object Python handler."""
    received: list[str] = []
    scene = None
    box = None

    @ui.page('/')
    def page():
        nonlocal scene, box
        with ui.scene() as scene:
            box = scene.box().on_pointer_over(lambda e: received.append(f'over:{e.object_id}'))

    screen.open('/')
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'const el = getElement({scene.id}); return el && !!el.renderer'
    ))
    # Synthesize the event directly on the element. Bypasses the actual pointer raycast,
    # but exercises the Python dispatch path end-to-end.
    screen.selenium.execute_script(
        f'getElement({scene.id}).$emit("pointerevent", {{'
        f'  type: "pointerover", object_id: "{box.id}", object_name: "",'
        '  button: 0, alt_key: false, ctrl_key: false, meta_key: false, shift_key: false,'
        '  x: 0, y: 0, z: 0, wx: 0, wy: 0, wz: 0,'
        '});'
    )
    screen.wait_for(lambda: any('over:' in msg for msg in received))
    assert received == [f'over:{box.id}']


def _viewport_point(screen: Screen, scene: ui.scene, x: float, y: float, z: float) -> tuple[int, int]:
    return screen.selenium.execute_script(
        f'const el = getElement({scene.id});'
        f'const p = el.camera.position.clone().set({x}, {y}, {z}).project(el.camera);'
        'const r = el.renderer.domElement.getBoundingClientRect();'
        'return [Math.round(r.left + (p.x + 1) / 2 * r.width), Math.round(r.top + (1 - p.y) / 2 * r.height)];'
    )


def test_dragging_transform_controls(screen: Screen):
    ends: list[tuple[float, float]] = []
    misses: list[str] = []
    scene = None
    box = None

    @ui.page('/')
    def page():
        nonlocal scene, box
        with ui.scene(on_transform_end=lambda e: ends.append((e.x, box.x)),
                      on_pointer_missed=lambda e: misses.append(e.type)) as scene:
            box = scene.box().on_click(lambda _: None)
        box.enable_transform_controls()

    screen.open('/')
    screen.wait_for_js(f'getElement({scene.id}).has_transform_controls("{box.id}")', True)
    x, y = _viewport_point(screen, scene, 1, 0, 0)  # on the X arrow, past the box
    actions = ActionBuilder(screen.selenium)
    actions.pointer_action.move_to_location(x, y).pointer_down().move_to_location(x + 30, y) \
        .move_to_location(x + 60, y).pointer_up()
    actions.perform()
    screen.wait_for(lambda: ends)
    reported_x, object_x = ends[0]
    assert reported_x > 0
    assert object_x == reported_x

    x, y = _viewport_point(screen, scene, -2, 0, 0)
    actions = ActionBuilder(screen.selenium)
    actions.pointer_action.move_to_location(x, y).click()
    actions.perform()
    screen.wait_for(lambda: 'click' in misses)
    assert misses == ['pointerdown', 'click'], 'grabbing the gizmo is not a miss, only the click into empty space is'


def test_clicking_an_object_with_transform_controls(screen: Screen):
    hits: list[list[str]] = []
    scene = None
    box = None

    @ui.page('/')
    def page():
        nonlocal scene, box
        with ui.scene(on_click=lambda e: hits.append([hit.object_id for hit in e.hits])) as scene:
            box = scene.box()
        box.enable_transform_controls()

    screen.open('/')
    screen.wait_for_js(f'getElement({scene.id}).has_transform_controls("{box.id}")', True)
    x, y = _viewport_point(screen, scene, 0.3, 0.3, 0.5)
    actions = ActionBuilder(screen.selenium)
    actions.pointer_action.move_to_location(x, y).click()
    actions.perform()
    screen.wait_for(lambda: hits)
    assert hits == [[box.id, 'ground']]


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


async def test_scene_is_collected_after_client_deletion(user: User):
    held = []  # stands in for a timer or handler holding the scene
    objects: weakref.WeakSet = weakref.WeakSet()

    @ui.page('/')
    def page():
        scene = ui.scene()
        held.append(scene)
        objects.add(scene)

    await user.open('/')
    user.client.delete()
    objects.add(held[0].box())  # late access after the client is gone
    held.clear()  # the timer finishes and drops its reference
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
