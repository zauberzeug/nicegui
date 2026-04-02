"""Tests for native window icon functionality."""

import inspect
import sys
from pathlib import Path

import pytest

from nicegui.native import window_icon
from nicegui.native.native_mode import activate


def test_find_window_by_title_returns_none_for_nonexistent_title():
    assert window_icon.find_window_by_title('NonExistentWindowTitle_12345_xyz') is None


def test_set_window_icon_windows_returns_false_on_non_windows():
    if sys.platform == 'win32':
        pytest.skip('Windows-only test for False case')
    assert window_icon.set_window_icon_windows(0, '/any/path.ico') is False


@pytest.mark.skipif(sys.platform != 'win32', reason='Windows-only')
def test_set_window_icon_windows_returns_false_for_nonexistent_file():
    assert window_icon.set_window_icon_windows(0, '/nonexistent/path/icon.ico') is False


@pytest.mark.skipif(sys.platform != 'win32', reason='Windows-only')
def test_set_window_icon_windows_with_invalid_hwnd_does_not_crash():
    path = Path(__file__).parent.parent / 'nicegui' / 'static' / 'favicon.ico'
    if not path.exists():
        pytest.skip('favicon.ico not found')
    assert isinstance(window_icon.set_window_icon_windows(0, str(path)), bool)


def test_activate_accepts_favicon_parameter():
    assert 'favicon' in (sig := inspect.signature(activate)).parameters
    assert sig.parameters['favicon'].default is None
