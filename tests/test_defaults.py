from nicegui import ui
import pytest



@pytest.fixture(autouse=True)
def enable_csp_for_module(enable_csp):
    """Enable CSP for all tests in this module to verify CSP compatibility."""
    yield




def test_default_props():
    @ui.page('/')
    def page():
        assert ui.button().props['color'] == 'primary', 'primary is the default color'

        ui.button.default_props('color=red')

        assert ui.button().props['color'] == 'red', 'if no color is passed, the default prop is used'
        assert ui.button(color='blue').props['color'] == 'blue', 'if a color is passed, it overrides the default prop'
        assert ui.button(color='primary').props['color'] == 'primary', 'even the default overrides the default prop'
