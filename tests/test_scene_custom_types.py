import os
import time
from pathlib import Path

import pytest

from nicegui import ui
from nicegui.elements.scene import Object3D
from nicegui.testing import Screen, User


class Tracer(Object3D, component='test_scene_custom_types.js'):
    def __init__(self, label: str) -> None:
        super().__init__(label)

    def set_value(self, value: int) -> None:
        self.run_method('set_value', value)


def test_custom_type_create_and_method_dispatch(screen: Screen):
    scene: ui.scene = None  # type: ignore

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            first = Tracer('first').with_name('a')
            Tracer('second').with_name('b')
        ui.button('Set value to 3', on_click=lambda: first.set_value(3))

    screen.open('/')
    screen.wait_for_js(f'scene_{scene.id}.getObjectByName("a")?.userData.label', 'first')
    screen.wait_for_js(f'scene_{scene.id}.getObjectByName("b")?.userData.label', 'second')
    screen.wait_for_js('window.__tracer_load_count', 1)  # the module top-level runs only once for multiple instances

    screen.click('Set value to 3')
    screen.wait_for_js(f'scene_{scene.id}.getObjectByName("a").scale.x', 3)
    screen.wait_for_js(f'scene_{scene.id}.getObjectByName("b").scale.x', 1)  # dispatch only reaches instance "a"


def test_two_classes_sharing_one_component(screen: Screen):
    class Marker(Object3D, component='test_scene_custom_types.js'):
        def __init__(self, label: str) -> None:
            super().__init__(label)

    scene: ui.scene = None  # type: ignore

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            Tracer('first').with_name('a')
            Marker('second').with_name('b')

    screen.open('/')
    screen.wait_for_js(f'scene_{scene.id}.getObjectByName("a")?.userData.label', 'first')
    screen.wait_for_js(f'scene_{scene.id}.getObjectByName("b")?.userData.label', 'second')


def test_class_registered_after_page_render(screen: Screen):
    scene: ui.scene = None  # type: ignore

    @ui.page('/')
    def page():
        nonlocal scene

        def create_late_object():
            class LateBox(Object3D, component='test_scene_custom_types_late.js'):
                pass
            with scene:
                LateBox(0.5).with_name('late')

        scene = ui.scene()
        ui.button('Create', on_click=create_late_object)

    screen.open('/')
    screen.click('Create')
    screen.wait_for_js(f'scene_{scene.id}.getObjectByName("late")?.geometry.parameters.width', 0.5)


def test_component_file_must_exist():
    with pytest.raises(ValueError, match=r'`component` must be an existing file, but "missing\.js" was not found'):
        class Missing(Object3D, component='missing.js'):  # pylint: disable=unused-variable
            pass


def test_subclass_without_component_raises():
    with pytest.raises(TypeError, match='without a `component` parameter'):
        class Bare(Object3D):  # pylint: disable=unused-variable
            pass


async def test_editing_a_component_file_keeps_its_page_working(user: User, tmp_path: Path) -> None:
    """Editing a component's JS while the server runs must not break the page that defines the class."""
    component = tmp_path / 'editable.js'
    component.write_text('export default {create_geometry: (THREE) => new THREE.BoxGeometry(1, 1, 1)};')

    @ui.page('/')
    def page():
        class Editable(Object3D, component=component):
            pass
        with ui.scene():
            Editable().with_name('editable')

    await user.open('/')
    component.write_text('export default {create_geometry: (THREE) => new THREE.BoxGeometry(2, 2, 2)};')
    os.utime(component, (time.time() + 1, time.time() + 1))
    await user.open('/')
