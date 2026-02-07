from nicegui import ui
from nicegui.testing import Screen
import pytest



@pytest.fixture(autouse=True)
def enable_csp_for_module(enable_csp):
    """Enable CSP for all tests in this module to verify CSP compatibility."""
    yield




def test_rating_click(screen: Screen):
    @ui.page('/')
    def page():
        rating = ui.rating(value=2)
        ui.label().bind_text_from(rating, 'value', lambda x: f'Value: {x}')

    screen.open('/')
    rating_icons = screen.find_all_by_class('q-rating__icon-container')
    rating_icons[0].click()
    screen.should_contain('Value: 1')

    rating_icons[3].click()
    screen.should_contain('Value: 4')

    rating_icons[3].click()  # already selected, should unselect
    screen.should_contain('Value: 0')
