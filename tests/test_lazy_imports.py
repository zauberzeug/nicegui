import subprocess
import sys
from textwrap import dedent
from types import ModuleType

import pytest

import nicegui
from nicegui import ui


@pytest.fixture(params=[nicegui, ui], ids=['nicegui', 'ui'])
def module(request: pytest.FixtureRequest) -> ModuleType:
    return request.param


def test_lazy_imports_match_all(module: ModuleType):
    assert set(module._LAZY_IMPORTS) == set(module.__all__)  # pylint: disable=protected-access


def test_all_names_resolve(module: ModuleType):
    for name in module.__all__:
        obj = getattr(module, name)
        assert obj is not None, f'{module.__name__}.{name} should not be None'


def test_dir_returns_expected_names(module: ModuleType):
    module_dir = dir(module)
    for name in module.__all__:
        assert name in module_dir, f'{name!r} should be in dir({module.__name__})'
    assert '__file__' in module_dir, f'dir({module.__name__}) should also list the module globals'


def test_nonexistent_attribute_raises(module: ModuleType):
    with pytest.raises(AttributeError, match=rf"module '{module.__name__}' has no attribute 'invalid_name'"):
        _ = module.invalid_name


def test_import_does_not_import_web_framework(module: ModuleType):
    result = subprocess.run([sys.executable, '-c', dedent(f'''\
        import sys
        import {module.__name__}
        heavy = {{'fastapi', 'starlette', 'socketio', 'engineio', 'uvicorn', 'matplotlib', 'httpx'}}
        loaded = heavy & set(sys.modules)
        sys.exit(f'unexpectedly imported: {{loaded}}' if loaded else 0)
    ''')], capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


def test_package_app_is_the_app_instance():
    from nicegui.app.app import App
    assert isinstance(nicegui.app, App), 'nicegui.app must be the App instance, not the nicegui.app subpackage'


@pytest.mark.parametrize('name', ['app', 'context'])
def test_package_objects_can_be_monkeypatched(name: str):
    from unittest import mock
    original = getattr(nicegui, name)
    with mock.patch.object(nicegui, name) as fake:
        assert getattr(nicegui, name) is fake
    assert getattr(nicegui, name) is original


def test_lazy_objects_win_over_submodule_shadowing():
    result = subprocess.run([sys.executable, '-c', dedent('''\
        import nicegui.context  # import submodules FIRST so the import machinery sets the package attributes...
        import nicegui.nicegui
        from nicegui import app, context  # ...which must NOT shadow the actual objects
        assert type(context).__name__ == 'Context', f'expected Context instance, got {type(context)}'
        assert type(app).__name__ == 'App', f'expected App instance, got {type(app)}'
    ''')], capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


def test_submodules_are_accessible_as_package_attributes():
    result = subprocess.run([sys.executable, '-c', dedent('''\
        import nicegui  # no submodule imported yet, so these attributes can only come from the package __getattr__
        assert nicegui.events.ClickEventArguments is not None
        assert nicegui.version.__version__ == nicegui.__version__
    ''')], capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


def test_every_submodule_can_be_imported_first():
    result = subprocess.run([sys.executable, '-c', dedent('''\
        import pkgutil
        import sys
        from importlib import import_module

        import nicegui
        names = [name for _, name, _ in pkgutil.walk_packages(nicegui.__path__, 'nicegui.')]
        assert names, 'the sweep found no submodules at all'
        failures = []
        for name in names:
            for module in [key for key in sys.modules if key.startswith('nicegui')]:
                del sys.modules[module]
            try:
                import_module(name)  # a lazy package must not depend on which submodule is imported first
            except ModuleNotFoundError as e:
                if not (e.name or '').startswith('nicegui'):
                    continue  # a missing optional dependency is not our concern here
                failures.append(f'{name}: {e}')
            except Exception as e:
                failures.append(f'{name}: {type(e).__name__}: {e}')
        sys.exit('\\n'.join(failures) if failures else 0)
    ''')], capture_output=True, text=True, timeout=300, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


def test_module_access_does_not_import_others():
    result = subprocess.run([sys.executable, '-c', dedent('''\
        import sys
        from nicegui import ui
        ui.label
        sys.exit('button' in sys.modules.keys())
    ''')], capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, 'button should not be imported when accessing label'
