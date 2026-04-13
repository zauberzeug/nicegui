import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from nicegui import ui
from nicegui.testing import Screen


def _drag(screen: Screen, source: WebElement, target: WebElement, *, dx: int = 0, dy: int = 0) -> None:
    ActionChains(screen.selenium) \
        .move_to_element(source) \
        .click_and_hold() \
        .move_to_element_with_offset(target, dx, dy) \
        .release() \
        .perform()


def _assert_order(screen: Screen, cls: str, expected: list[str]) -> None:
    assert screen.find_by_class(cls).text.splitlines() == expected


def test_basic_reorder(screen: Screen):
    @ui.page('/')
    def page():
        with ui.card().classes('card') as card:
            ui.label('A')
            ui.label('B')
            ui.label('C')

        card.make_sortable(on_end=lambda e: ui.notify(
            f'{e.item._text} moved from index {e.old_index} to {e.new_index}'  # pylint: disable=protected-access
        ))

    screen.open('/')
    _drag(screen, screen.find('A'), screen.find('B'), dy=5)
    _assert_order(screen, 'card', ['B', 'A', 'C'])
    screen.should_contain('A moved from index 0 to 1')


def test_cross_container(screen: Screen):
    @ui.page('/')
    def page():
        with ui.row():
            with ui.card().classes('card1') as card1:
                ui.label('A')
                ui.label('B')
            with ui.card().classes('card2') as card2:
                ui.label('C')

        card1.make_sortable(group='shared', on_end=lambda e: ui.notify(
            f'Card1: {e.item._text} moved from index {e.old_index} to {e.new_index}'  # pylint: disable=protected-access
        ))
        card2.make_sortable(group='shared', on_end=lambda: ui.notify('Card2: something move_end'))

    screen.open('/')
    _drag(screen, screen.find('A'), screen.find('C'), dy=-5)
    _assert_order(screen, 'card1', ['B'])
    _assert_order(screen, 'card2', ['A', 'C'])
    screen.should_contain('Card1: A moved from index 0 to 0')
    screen.should_not_contain('Card2: something moved')  # because the event only fires on the source container


def test_disable_and_enable(screen: Screen):
    @ui.page('/')
    def page():
        with ui.card().classes('card') as card:
            ui.label('A')
            ui.label('B')
            ui.label('C')
        sortable = card.make_sortable()
        ui.button('Disable', on_click=sortable.disable)
        ui.button('Enable', on_click=sortable.enable)

    screen.open('/')
    _drag(screen, screen.find('A'), screen.find('B'), dy=5)
    _assert_order(screen, 'card', ['B', 'A', 'C'])

    screen.click('Disable')
    _drag(screen, screen.find('B'), screen.find('A'), dy=5)
    _assert_order(screen, 'card', ['B', 'A', 'C'])

    screen.click('Enable')
    _drag(screen, screen.find('B'), screen.find('A'), dy=5)
    _assert_order(screen, 'card', ['A', 'B', 'C'])


def test_handle_property(screen: Screen):
    @ui.page('/')
    def page():
        with ui.card().classes('card') as card:
            ui.label('A')
            ui.label('B')
            ui.label('C')
        sortable = card.make_sortable(handle='.handle')
        ui.button('Remove handle', on_click=lambda: setattr(sortable, 'handle', None))

    screen.open('/')
    _drag(screen, screen.find('A'), screen.find('B'), dy=5)
    _assert_order(screen, 'card', ['A', 'B', 'C'])

    screen.click('Remove handle')
    _drag(screen, screen.find('A'), screen.find('B'), dy=5)
    _assert_order(screen, 'card', ['B', 'A', 'C'])


def test_make_sortable_twice_raises(screen: Screen):
    @ui.page('/')
    def page():
        col = ui.column()
        col.make_sortable()
        with pytest.raises(RuntimeError, match='already sortable'):
            col.make_sortable()

    screen.open('/')
