from unittest.mock import patch

import pytest

from nicegui import events, ui
from nicegui.testing import Screen


@pytest.mark.parametrize('require_escape_hold', [True, False])
def test_fullscreen_creation(screen: Screen, require_escape_hold: bool):
    fullscreen = ui.fullscreen(require_escape_hold=require_escape_hold)
    assert not fullscreen.state
    assert fullscreen.require_escape_hold == require_escape_hold

    screen.open('/')


def test_fullscreen_state_change(screen: Screen):
    states = []

    fullscreen = ui.fullscreen(on_state_change=lambda e: states.append(e.value))

    screen.open('/')

    event_args = events.GenericEventArguments(sender=fullscreen, client=fullscreen.client, args=True)
    fullscreen._handle_fullscreen_change(event_args)
    assert states == [True]
    assert fullscreen.state

    event_args = events.GenericEventArguments(sender=fullscreen, client=fullscreen.client, args=False)
    fullscreen._handle_fullscreen_change(event_args)
    assert states == [True, False]
    assert not fullscreen.state


def test_fullscreen_methods(screen: Screen):
    fullscreen = ui.fullscreen(require_escape_hold=True)

    screen.open('/')

    with patch.object(fullscreen, 'run_method') as mock_run:
        fullscreen.enter()
        mock_run.assert_called_once_with('enter', True)
        mock_run.reset_mock()

        fullscreen.exit()
        mock_run.assert_called_once_with('exit')
        mock_run.reset_mock()

        fullscreen.toggle()
        mock_run.assert_called_once_with('toggle', True)
        mock_run.reset_mock()

        fullscreen.state = True
        mock_run.assert_called_once_with('enter', True)
        mock_run.reset_mock()

        fullscreen.state = False
        mock_run.assert_called_once_with('exit')
        mock_run.reset_mock()


def test_fullscreen_button_click(screen: Screen):
    """Test that clicking a button to enter fullscreen creates the correct JavaScript call.

    Note: We cannot test actual fullscreen behavior as it requires user interaction,
    but we can verify the JavaScript method is called correctly.
    """
    result = []

    fullscreen = ui.fullscreen(on_state_change=lambda e: result.append(e.value))
    ui.button('Enter Fullscreen', on_click=fullscreen.enter)
    ui.button('Exit Fullscreen', on_click=fullscreen.exit)

    screen.open('/')
    screen.click('Enter Fullscreen')
    screen.wait(0.5)
    assert result == [True]
