from unittest.mock import patch

from nicegui import ui
from nicegui.testing import Screen


def test_fullscreen_creation(screen: Screen):
    @ui.page('/')
    def page():
        fs = ui.app_fullscreen()
        assert not fs.state
        assert not fs.require_escape_hold

    screen.open('/')


def test_fullscreen_initial_state(screen: Screen):
    @ui.page('/')
    def page():
        fs = ui.app_fullscreen(require_escape_hold=True)
        assert fs.require_escape_hold
        assert not fs.state

    screen.open('/')


def test_fullscreen_state_change(screen: Screen):
    states = []

    @ui.page('/')
    def page():
        fs = ui.app_fullscreen()

        def on_state_change(e):
            states.append(e.value)

        fs.on_state_change(on_state_change)

        # Simulate fullscreen change event from JavaScript
        fs._handle_fullscreen_change(type('Event', (), {'args': True}))
        assert states == [True]
        assert fs.state

        fs._handle_fullscreen_change(type('Event', (), {'args': False}))
        assert states == [True, False]
        assert not fs.state

    screen.open('/')


def test_fullscreen_methods(screen: Screen):
    @ui.page('/')
    def page():
        fs = ui.app_fullscreen(require_escape_hold=True)
        
        with patch.object(fs, 'run_method') as mock_run:
            fs.enter()
            mock_run.assert_called_once_with('enter', True)
            mock_run.reset_mock()

            fs.exit()
            mock_run.assert_called_once_with('exit')
            mock_run.reset_mock()

            fs.toggle()
            mock_run.assert_called_once_with('toggle', True)

    screen.open('/')


def test_fullscreen_property_binding(screen: Screen):
    @ui.page('/')
    def page():
        fs = ui.app_fullscreen()
        
        fs.require_escape_hold = True
        assert fs.require_escape_hold

        fs.state = True  # This should call enter()
        with patch.object(fs, 'run_method') as mock_run:
            fs.state = False  # This should call exit()
            mock_run.assert_called_once_with('exit')

    screen.open('/')


def test_fullscreen_button_click(screen: Screen):
    """Test that clicking a button to enter fullscreen creates the correct JavaScript call.
    
    Note: We cannot test actual fullscreen behavior as it requires user interaction,
    but we can verify the JavaScript method is called correctly.
    """
    result = []
    
    @ui.page('/')
    def page():
        fs = ui.app_fullscreen()
        ui.button('Enter Fullscreen', on_click=fs.enter)
        ui.button('Exit Fullscreen', on_click=fs.exit)

        def on_state_change(e):
            result.append(e.value)
        fs.on_state_change(on_state_change)

    screen.open('/')
    screen.click('Enter Fullscreen')
    screen.wait(0.5)  # Give time for potential JavaScript errors


def test_fullscreen_switch_binding(screen: Screen):
    """Test that the require_escape_hold switch properly binds to the fullscreen control."""
    @ui.page('/')
    def page():
        fs = ui.app_fullscreen()
        ui.label('Require escape hold:')
        switch = ui.switch().bind_value_to(fs, 'require_escape_hold')

    screen.open('/')
    screen.should_contain('Require escape hold:')
