import importlib
import subprocess
from textwrap import dedent

import pytest

from nicegui import ui


def test_all_names_resolve():
    for name in ui.__all__:
        obj = getattr(ui, name)
        assert obj is not None, f'ui.{name} resolved to None'


def test_dir_returns_expected_names():
    ui_dir = dir(ui)
    for name in ui.__all__:
        assert name in ui_dir, f'{name!r} missing from dir(ui)'


def test_nonexistent_attribute_raises():
    with pytest.raises(AttributeError, match='no_such_widget'):
        _ = ui.no_such_widget


def test_heavy_modules_not_imported_on_lightweight_access():
    """Accessing a lightweight element like ui.label should not pull in heavy optional dependencies."""
    result = subprocess.run(['python3', '-c', dedent('''\
        import sys
        from nicegui import ui
        ui.label
        sys.exit(bool({"plotly", "pyecharts", "pandas", "matplotlib"} & sys.modules.keys()))
    ''')], capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, 'Heavy modules were imported after accessing ui.label'


def test_lazy_imports_match_all():
    mod = importlib.import_module('nicegui.ui')
    lazy = set(mod._LAZY_IMPORTS)
    all_set = set(mod.__all__)
    assert lazy == all_set, f'Mismatch: only in _LAZY_IMPORTS={lazy - all_set}, only in __all__={all_set - lazy}'
