import sys

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
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("a")?.userData.label', 'first')
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("b")?.userData.label', 'second')
    screen.wait_for_js('window.__tracer_load_count', 1)  # the module top-level runs only once for multiple instances

    screen.click('Set value to 3')
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("a").scale.x', 3)
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("b").scale.x', 1)  # dispatch only reaches instance "a"


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
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("a")?.userData.label', 'first')
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("b")?.userData.label', 'second')


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
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("late")?.geometry.parameters.width', 0.5)


def test_component_file_must_exist():
    with pytest.raises(ValueError, match=r'`component` must be an existing file, but "missing\.js" was not found'):
        class Missing(Object3D, component='missing.js'):  # pylint: disable=unused-variable
            pass


def test_deprecated_scene_objects_module_keeps_working(screen: Screen):
    """Deep imports from the removed scene_objects module must keep working with a deprecation warning."""
    sys.modules.pop('nicegui.elements.scene.scene_objects', None)
    from nicegui.elements.scene.objects.group import Group as CanonicalGroup  # pylint: disable=import-outside-toplevel
    from nicegui.elements.scene.scene_objects import Group  # pylint: disable=import-outside-toplevel
    assert Group is CanonicalGroup
    screen.assert_py_logger('WARNING',
                            'The module `nicegui.elements.scene.scene_objects` is deprecated and will be removed in NiceGUI 4.0. '
                            'Import scene objects from `nicegui.elements.scene.objects` instead.')


def test_bare_subclass_with_legacy_type_string_creates_group(screen: Screen):
    class LegacyObject(Object3D):
        def __init__(self) -> None:
            super().__init__('group')

    scene: ui.scene = None  # type: ignore

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            with LegacyObject().with_name('legacy'):
                scene.box().with_name('child')

    screen.open('/')
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("legacy")?.type', 'Group')
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("legacy")?.getObjectByName("child")?.type', 'Mesh')


def test_legacy_type_string_consumes_a_trailing_wireframe_flag(screen: Screen):
    scene: ui.scene = None  # type: ignore

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            Object3D('box', 1, 2, 3, True).with_name('wireframe')
            Object3D('box', 1, 2, 3).with_name('solid')

    screen.open('/')
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("wireframe")?.type', 'LineSegments')
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("solid")?.geometry.parameters.depth', 3)


async def test_deprecated_type_property_reports_the_legacy_type_string(user: User, caplog: pytest.LogCaptureFixture) -> None:
    types: list[str | None] = []

    @ui.page('/')
    def page():
        with ui.scene() as scene:
            types.append(scene.box().type)
            types.append(Object3D('group').type)

    await user.open('/')
    assert types == ['box', 'group']
    assert any('The `type` property of `Object3D` is deprecated' in record.message for record in caplog.records)


async def test_unknown_legacy_type_string_raises(user: User) -> None:
    errors: list[str] = []

    @ui.page('/')
    def page():
        with ui.scene():
            try:
                Object3D('teapot')
            except TypeError as e:
                errors.append(str(e))

    await user.open('/')
    assert errors == ['Unknown object type "teapot".']
