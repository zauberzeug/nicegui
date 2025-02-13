from nicegui import ui
from nicegui.testing import Screen


def test_rating_click(screen: Screen):
    rating = ui.rating(value=2)
    ui.label().bind_text_from(rating, 'value', lambda x: f'Value: {x}')

    screen.open('/')
    rating_icons = screen.find_all_by_class('q-rating__icon-container')
    rating_icons[0].click()
    screen.should_contain('Value: 1')

    rating_icons[3].click()
    screen.should_contain('Value: 4')

    rating_icons[3].click()  # already selected, should unselect
    screen.wait(0.5)
    screen.should_contain('Value: 0')
