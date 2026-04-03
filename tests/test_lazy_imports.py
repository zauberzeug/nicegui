import importlib

import pytest


def test_all_names_resolve():
    from nicegui import ui

    for name in ui.__all__:
        obj = getattr(ui, name)
        assert obj is not None, f'ui.{name} resolved to None'


def test_dir_returns_expected_names():
    from nicegui import ui

    ui_dir = dir(ui)
    for name in ui.__all__:
        assert name in ui_dir, f'{name!r} missing from dir(ui)'


def test_nonexistent_attribute_raises():
    from nicegui import ui

    with pytest.raises(AttributeError, match='no_such_widget'):
        _ = ui.no_such_widget


def test_lazy_imports_match_all():
    mod = importlib.import_module('nicegui.ui')
    lazy = set(mod._LAZY_IMPORTS)
    all_set = set(mod.__all__)
    assert lazy == all_set, f'Mismatch: only in _LAZY_IMPORTS={lazy - all_set}, only in __all__={all_set - lazy}'
