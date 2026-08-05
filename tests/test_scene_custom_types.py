import logging
import sys

import pytest
from typing_extensions import Self

from nicegui import ui
from nicegui.elements.scene import Object3D
from nicegui.testing import Screen


class Tracer(Object3D, component='test_scene_custom_types.js'):
    def __init__(self, label: str) -> None:
        super().__init__(label)

    def set_value(self, value: int) -> Self:
        self.run_method('set_value', value)
        return self


def test_custom_type_create_and_method_dispatch(screen: Screen):
    scene: ui.scene = None  # type: ignore
    tracer: Tracer = None  # type: ignore

    @ui.page('/')
    def page():
        nonlocal scene, tracer
        with ui.scene() as scene:
            tracer = Tracer('first').with_name('a')
            Tracer('second').with_name('b')

    screen.open('/')
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("a")?.userData.label', 'first')
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("b")?.userData.label', 'second')
    assert screen.selenium.execute_script('return window.__tracer_load_count') == 1, \
        'the module top-level should run only once for multiple instances'

    tracer.set_value(3)
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("a").scale.x', 3)
    assert screen.selenium.execute_script(f'return scene_{scene.html_id}.getObjectByName("b").scale.x') == 1, \
        'the method dispatch should only reach the targeted instance'


def test_component_file_must_exist():
    """component= must point to an existing file; a missing one raises ValueError at class-definition time."""
    with pytest.raises(ValueError, match='was not found'):
        class Missing(Object3D, component='missing.js'):
            pass


class LegacyObject(Object3D):  # RoSys-style bare subclass (no component=), works via deprecation shims until 4.0
    def __init__(self) -> None:
        super().__init__('group')


def test_deprecated_scene_objects_module_keeps_working(caplog: pytest.LogCaptureFixture):
    """RoSys-style deep imports from the removed scene_objects module must keep working with a deprecation warning."""
    sys.modules.pop('nicegui.elements.scene.scene_objects', None)
    with caplog.at_level(logging.WARNING):
        from nicegui.elements.scene.scene_objects import Group  # pylint: disable=import-outside-toplevel
    from nicegui.elements.scene.objects.group import Group as CanonicalGroup  # pylint: disable=import-outside-toplevel
    assert Group is CanonicalGroup
    assert any('scene_objects' in record.message and 'deprecated' in record.message for record in caplog.records), \
        'importing the legacy module should log a deprecation warning'


def test_bare_subclass_with_legacy_type_string_creates_group(screen: Screen):
    scene: ui.scene = None  # type: ignore

    @ui.page('/')
    def page():
        nonlocal scene
        with ui.scene() as scene:
            with LegacyObject().with_name('legacy'):
                scene.box().with_name('child')

    screen.open('/')
    screen.wait_for_js(f'scene_{scene.html_id}.getObjectByName("legacy")?.getObjectByName("child")?.type', 'Mesh')
    group_type = screen.selenium.execute_script(f'return scene_{scene.html_id}.getObjectByName("legacy")?.type')
    assert group_type == 'Group'


def test_unknown_legacy_type_string_raises(screen: Screen):
    errors: list[str] = []

    @ui.page('/')
    def page():
        with ui.scene():
            try:
                Object3D('teapot')
            except TypeError as e:
                errors.append(str(e))

    screen.open('/')
    assert errors == ['Unknown object type "teapot".']
