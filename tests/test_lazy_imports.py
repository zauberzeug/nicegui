import subprocess
import sys
from textwrap import dedent

import pytest

import nicegui
from nicegui import ui


def test_lazy_imports_match_all():
    assert set(ui._LAZY_IMPORTS) == set(ui.__all__)  # pylint: disable=protected-access


def test_package_lazy_imports_match_all():
    assert set(nicegui._LAZY_IMPORTS) == set(nicegui.__all__)  # pylint: disable=protected-access


def test_package_all_names_resolve():
    for name in nicegui.__all__:
        obj = getattr(nicegui, name)
        assert obj is not None, f'nicegui.{name} should not be None'


def test_package_app_is_the_app_instance():
    from nicegui.app.app import App
    assert isinstance(nicegui.app, App), 'nicegui.app must be the App instance, not the nicegui.app subpackage'


def test_package_app_and_context_can_be_monkeypatched():
    from unittest import mock
    original = nicegui.app
    with mock.patch.object(nicegui, 'app') as fake:
        assert nicegui.app is fake
    assert nicegui.app is original


def test_lazy_objects_win_over_submodule_shadowing():
    result = subprocess.run([sys.executable, '-c', dedent('''\
        import nicegui.context  # import submodules FIRST so the import machinery sets the package attributes...
        import nicegui.nicegui
        from nicegui import app, context  # ...which must NOT shadow the actual objects
        assert type(context).__name__ == 'Context', f'expected Context instance, got {type(context)}'
        assert type(app).__name__ == 'App', f'expected App instance, got {type(app)}'
    ''')], capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


def test_package_import_does_not_import_web_framework():
    result = subprocess.run([sys.executable, '-c', dedent('''\
        import sys
        import nicegui
        heavy = {'fastapi', 'starlette', 'socketio', 'engineio', 'uvicorn', 'matplotlib', 'httpx'}
        loaded = heavy & set(sys.modules)
        sys.exit(f'unexpectedly imported: {loaded}' if loaded else 0)
    ''')], capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


def test_ui_import_does_not_import_web_framework():
    result = subprocess.run([sys.executable, '-c', dedent('''\
        import sys
        from nicegui import ui
        heavy = {'fastapi', 'starlette', 'socketio', 'engineio', 'uvicorn', 'matplotlib', 'httpx'}
        loaded = heavy & set(sys.modules)
        sys.exit(f'unexpectedly imported: {loaded}' if loaded else 0)
    ''')], capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


def test_all_names_resolve():
    for name in ui.__all__:
        obj = getattr(ui, name)
        assert obj is not None, f'ui.{name} should not be None'


def test_dir_returns_expected_names():
    ui_dir = dir(ui)
    for name in ui.__all__:
        assert name in ui_dir, f'{name!r} should be in dir(ui)'


def test_nonexistent_attribute_raises():
    with pytest.raises(AttributeError, match=r"module 'nicegui\.ui' has no attribute 'invalid_name'"):
        _ = ui.invalid_name


def test_module_access_does_not_import_others():
    result = subprocess.run(['python3', '-c', dedent('''\
        import sys
        from nicegui import ui
        ui.label
        sys.exit('button' in sys.modules.keys())
    ''')], capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, 'button should not be imported when accessing label'
