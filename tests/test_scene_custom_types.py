from pathlib import Path
from unittest.mock import patch

import pytest
from typing_extensions import Self

from nicegui import ui
from nicegui.elements.scene.scene_object3d import Object3D
from nicegui.testing import Screen


class Tracer(Object3D, component='tracer.js'):
    def __init__(self, label: str) -> None:
        super().__init__(label)

    def set_value(self, value: int) -> Self:
        self.run_method('set_value', value)
        return self


def test_custom_type_create_and_method_dispatch(screen: Screen):
    tracer: Tracer = None  # type: ignore

    @ui.page('/')
    def page():
        nonlocal tracer
        with ui.scene():
            tracer = Tracer('hello')

    screen.open('/')
    screen.wait(0.8)

    created = screen.selenium.execute_script('return window.__tracer.created')
    assert created is not None and len(created) == 1
    assert created[0]['label'] == 'hello'

    assert tracer is not None
    tracer.set_value(42)
    screen.wait(0.5)
    values = screen.selenium.execute_script('return window.__tracer.values')
    assert values and values[-1]['value'] == 42
    assert values[-1]['id'] == tracer.id


def test_custom_type_module_loads_once_for_multiple_instances(screen: Screen):
    @ui.page('/')
    def page():
        with ui.scene():
            Tracer('a')
            Tracer('b')

    screen.open('/')
    screen.wait(0.8)

    # Module top-level resets window.__tracer; two created entries proves the
    # module ran exactly once even though the class was instantiated twice.
    created = screen.selenium.execute_script('return window.__tracer.created')
    assert created is not None and len(created) == 2
    assert [c['label'] for c in created] == ['a', 'b']


def test_component_glob_matching_multiple_files_raises():
    """component= must resolve to exactly one file; a multi-file glob raises ValueError at class-definition time."""
    with patch('nicegui.elements.scene.scene_object3d.resolve_glob', return_value=[Path('a.js'), Path('b.js')]):
        with pytest.raises(ValueError, match='exactly one file'):
            class MultiMatch(Object3D, component='widgets/*.js'):
                pass


def test_subclass_without_component_still_registers_dependencies_and_esm():
    """Inheriting component= from a parent must not silently skip dependencies= and esm=."""
    with patch('nicegui.elements.scene.scene_object3d.resolve_glob', return_value=[Path('base.js')]), \
            patch('nicegui.elements.scene.scene_object3d.register_library_glob') as mock_lib, \
            patch('nicegui.elements.scene.scene_object3d.register_esm_glob') as mock_esm:

        class Base(Object3D, component='base.js'):
            pass

        mock_lib.reset_mock()
        mock_esm.reset_mock()

        class Child(Base, dependencies=['helper.js'], esm={'mykey': 'helper.esm.js'}):
            pass

        mock_lib.assert_called_once()
        assert mock_lib.call_args.args[0] == 'helper.js'
        assert mock_lib.call_args.kwargs.get('import_name') is None

        mock_esm.assert_called_once()
        assert mock_esm.call_args.args == ('mykey', 'helper.esm.js')
