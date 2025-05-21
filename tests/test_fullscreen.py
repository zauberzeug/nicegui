from unittest.mock import patch

import pytest

from nicegui import ui
from nicegui.testing import Screen


@pytest.mark.parametrize('require_escape_hold', [True, False])
def test_fullscreen_creation(screen: Screen, require_escape_hold: bool):
    fullscreen = ui.fullscreen(require_escape_hold=require_escape_hold)
    assert not fullscreen.value
    assert fullscreen.require_escape_hold == require_escape_hold

    screen.open('/')


def test_fullscreen_methods(screen: Screen):
    values = []

    fullscreen = ui.fullscreen(on_value_change=lambda e: values.append(e.value))

    screen.open('/')

    with patch.object(fullscreen, 'run_method') as mock_run:
        fullscreen.enter()
        mock_run.assert_called_once_with('enter')
        mock_run.reset_mock()

        fullscreen.exit()
        mock_run.assert_called_once_with('exit')
        mock_run.reset_mock()

        fullscreen.toggle()
        mock_run.assert_called_once_with('enter')
        mock_run.reset_mock()

        fullscreen.value = False
        mock_run.assert_called_once_with('exit')
        mock_run.reset_mock()

        fullscreen.value = True
        mock_run.assert_called_once_with('enter')
        mock_run.reset_mock()

    assert values == [True, False, True, False, True]


def test_fullscreen_button_click(screen: Screen):
    """Test that clicking a button to enter fullscreen creates the correct JavaScript call.

    Note: We cannot test actual fullscreen behavior as it requires user interaction,
    but we can verify the JavaScript method is called correctly.
    """
    values = []

    fullscreen = ui.fullscreen(on_value_change=lambda e: values.append(e.value))
    ui.button('Enter Fullscreen', on_click=fullscreen.enter)
    ui.button('Exit Fullscreen', on_click=fullscreen.exit)

    screen.open('/')
    screen.click('Enter Fullscreen')
    screen.wait(0.5)
    assert values == [True]

    screen.click('Exit Fullscreen')
    screen.wait(0.5)
    assert values == [True, False]
