import pytest

from nicegui.native.window_icon import _create_windows_app_id


@pytest.mark.parametrize('title, expected', [
    ('My App', 'nicegui.My_App'),
    ('NiceGUI', 'nicegui.NiceGUI'),
    ('hello world 123', 'nicegui.hello_world_123'),
    ('', 'nicegui.app'),
    ('!!!@@@###', 'nicegui.app'),
    ('  spaces  ', 'nicegui.spaces'),
    ('a' * 200, 'nicegui.' + 'a' * 120),
])
def test_create_windows_app_id(title: str, expected: str) -> None:
    assert _create_windows_app_id(title) == expected
