from nicegui import ui
from nicegui.testing import SharedScreen


def test_rating_click(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        rating = ui.rating(value=2)
        ui.label().bind_text_from(rating, 'value', lambda x: f'Value: {x}')

    shared_screen.open('/')
    rating_icons = shared_screen.find_all_by_class('q-rating__icon-container')
    rating_icons[0].click()
    shared_screen.should_contain('Value: 1')

    rating_icons[3].click()
    shared_screen.should_contain('Value: 4')

    rating_icons[3].click()  # already selected, should unselect
    shared_screen.should_contain('Value: 0')
