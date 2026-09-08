import subprocess
from textwrap import dedent

import pytest

from nicegui import ui


def test_lazy_imports_match_all():
    assert set(ui._LAZY_IMPORTS) == set(ui.__all__)  # pylint: disable=protected-access


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


def test_esm_modules_registered_on_import():
    result = subprocess.run(['python3', '-c', dedent('''\
        from pathlib import Path
        from nicegui import ui
        from nicegui.dependencies import esm_modules
        packages = {p.parent.name for p in Path(ui.__file__).parent.glob('elements/*/dist')}
        registered = {m.path.parent.name for m in esm_modules.values()}
        missing = packages - registered
        assert not missing, f'ESM modules not registered on import: {sorted(missing)}'
    ''')], capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stderr
