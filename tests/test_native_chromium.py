import importlib.util
import re
import sys
from pathlib import Path

import pytest

from nicegui.helpers import warnings
from nicegui.native import chromium


@pytest.fixture(autouse=True)
def forget_shown_warnings() -> None:
    warnings.reset()  # warn_once remembers across tests, which would hide expected messages


# The fallback backend stands in for pywebview, so it must provide everything NiceGUI uses from
# it. Deriving the expectation from the consuming modules keeps this honest: adding a new
# `webview.<name>` call to native mode fails this test until the fallback provides it too.
# That matters because a developer with pywebview installed never exercises the fallback, so a
# missing attribute would otherwise surface only for users who do not have the extra.
CONSUMERS = [Path(chromium.__file__).parent / name for name in ('native.py', 'native_mode.py')]

# Members of pywebview's Window this backend knowingly does not provide. UNSUPPORTED_METHODS
# warn and return; these are absent entirely. Kept explicit so that a new pywebview release
# adding an API forces a decision here rather than silently widening the gap.
KNOWN_ABSENT_WINDOW_MEMBERS = {'state'}


def _webview_attributes_used_by(path: Path) -> set[str]:
    """Names accessed as `webview.<name>` at runtime.

    Import statements are skipped: `from webview.window import ...` names a submodule that only
    the real pywebview branch ever resolves, so it is not part of the fallback's contract.
    """
    code = '\n'.join(line for line in path.read_text().splitlines()
                     if not line.lstrip().startswith(('import webview', 'from webview')))
    return set(re.findall(r'\bwebview\.([A-Za-z_][A-Za-z0-9_]*)', code))


@pytest.mark.parametrize('path', CONSUMERS, ids=lambda p: p.name)
def test_fallback_provides_what_native_mode_uses(path: Path) -> None:
    used = _webview_attributes_used_by(path)
    assert used, f'found no webview.* usage in {path.name}; has the parsing broken?'
    missing = sorted(name for name in used if not hasattr(chromium, name))
    assert not missing, f'{path.name} uses webview.{missing} but the fallback backend lacks it'


@pytest.mark.skipif(importlib.util.find_spec('webview') is None, reason='pywebview is not installed')
def test_fallback_covers_the_pywebview_window_api() -> None:
    import webview  # pylint: disable=import-outside-toplevel
    expected = {name for name in vars(webview.Window) if not name.startswith('_')}
    # properties are looked up on the class so that they are not evaluated here
    provided = {name for name in expected if hasattr(chromium.Window, name)}
    missing = expected - provided - chromium.UNSUPPORTED_METHODS - KNOWN_ABSENT_WINDOW_MEMBERS
    assert not missing, (f'pywebview offers Window.{sorted(missing)}, which the fallback neither '
                         'implements nor lists as unsupported')


@pytest.mark.parametrize('name', ['shown', 'loaded', 'closed', 'minimized',
                                  'maximized', 'restored', 'resized', 'moved'])
def test_window_exposes_the_events_native_mode_binds(name: str) -> None:
    assert hasattr(chromium.Window(url='http://127.0.0.1').events, name)


def test_dom_event_handlers_are_accepted() -> None:
    window = chromium.Window(url='http://127.0.0.1')
    window.dom.document.events.drop += chromium.DOMEventHandler(lambda _: None, True, False)


@pytest.mark.parametrize('name', sorted(chromium.UNSUPPORTED_METHODS))
def test_unsupported_methods_warn_instead_of_raising(name: str, caplog: pytest.LogCaptureFixture) -> None:
    window = chromium.Window(url='http://127.0.0.1')
    assert getattr(window, name)() is None
    assert f'does not support window.{name}()' in caplog.text


def test_unknown_attributes_still_raise() -> None:
    window = chromium.Window(url='http://127.0.0.1')
    with pytest.raises(AttributeError):
        _ = window.no_such_method


def test_ignored_window_args_are_reported(caplog: pytest.LogCaptureFixture) -> None:
    chromium.Window(url='http://127.0.0.1', resizable=False, min_size=(300, 300))
    assert 'does not support the window arguments' in caplog.text
    assert 'resizable' in caplog.text and 'min_size' in caplog.text


def test_honoured_window_args_are_not_reported(caplog: pytest.LogCaptureFixture) -> None:
    chromium.Window(url='http://127.0.0.1', x=60, y=60)
    assert 'does not support' not in caplog.text


def test_browser_can_be_selected_by_environment_variable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(chromium.BROWSER_ENV_VAR, sys.executable)
    assert chromium.find_browser() == sys.executable


def test_browser_path_is_expanded(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('NICEGUI_TEST_BROWSER_DIR', str(Path(sys.executable).parent))
    monkeypatch.setenv(chromium.BROWSER_ENV_VAR, '$NICEGUI_TEST_BROWSER_DIR/' + Path(sys.executable).name)
    assert chromium.find_browser() == sys.executable


def test_missing_browser_is_reported_as_none(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(chromium.BROWSER_ENV_VAR, 'definitely-not-an-installed-browser')
    assert chromium.find_browser() is None
