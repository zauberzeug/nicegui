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
            scene.gltf('/box.glb').material('#ff0000')

    screen.open('/')
    screen.wait(1.0)
    assert screen.selenium.execute_script(f'return scene_{scene.html_id}.children.length') == 5
    assert screen.selenium.execute_script(
        f'return scene_{scene.html_id}.children[4].getObjectByProperty("isMesh", true).material.color.getHexString()'
    ) == 'ff0000'


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
        f'const el = getElement({scene.id}); return el && el.is_initialized'
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
        f'const el = getElement({scene.id}); return el && el.is_initialized'
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
        f'const el = getElement({scene.id}); return el && el.is_initialized'
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


def test_interactive_payload_only_when_truthy(screen: Screen):
    """Plain objects' data length stays stable; objects with handlers or effects append a trailing dict."""
    scene = None
    plain = None
    handled = None
    glowed = None

    @ui.page('/')
    def page():
        nonlocal scene, plain, handled, glowed
        with ui.scene() as scene:
            plain = scene.box()
            handled = scene.box().on_pointer_over(lambda _: None)
            glowed = scene.box().hover_effect('glow', color='#ff0000')

    screen.open('/')
    assert len(handled.data) == len(plain.data) + 1
    assert handled.data[-1] == {'handlers': ['pointerover']}
    assert len(glowed.data) == len(plain.data) + 1
    assert glowed.data[-1] == {'effect': {'effect': 'glow', 'color': '#ff0000'}}


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
        f'const el = getElement({scene.id}); return el && el.is_initialized'
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
        f'const el = getElement({scene.id}); return el && el.is_initialized'
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
        f'const el = getElement({scene.id}); return el && el.is_initialized'
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
