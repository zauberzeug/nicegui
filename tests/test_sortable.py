import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from nicegui import events, ui
from nicegui.testing import Screen


def _drag(screen: Screen, source: WebElement, target: WebElement, *, dx: int = 0, dy: int = 0) -> None:
    ActionChains(screen.selenium) \
        .move_to_element(source) \
        .click_and_hold() \
        .move_to_element_with_offset(target, dx, dy) \
        .release() \
        .perform()


def test_basic_reorder(screen: Screen):
    @ui.page('/')
    def page():
        with ui.card() as card:
            ui.label('A')
            ui.label('B')
            ui.label('C')
        order = ui.label()

        def handle_end(e: events.SortableEventArguments):
            ui.notify(f'{e.item._text} moved from index {e.old_index} to {e.new_index}')  # pylint: disable=protected-access
            order.text = f'card: {", ".join(child._text or "" for child in card)}'  # pylint: disable=protected-access
        card.make_sortable(on_end=handle_end)

    screen.open('/')
    _drag(screen, screen.find('A'), screen.find('B'), dy=5)
    screen.should_contain('card: B, A, C')
    screen.should_contain('A moved from index 0 to 1')


def test_cross_container(screen: Screen):
    @ui.page('/')
    def page():
        with ui.row():
            with ui.card() as card1:
                ui.label('A')
                ui.label('B')
            with ui.card() as card2:
                ui.label('C')
        order1 = ui.label()
        order2 = ui.label()

        def handle_end_card1(e: events.SortableEventArguments):
            ui.notify(
                f'Card1: {e.item._text} moved from index {e.old_index} to {e.new_index}'  # pylint: disable=protected-access
            )
            order1.text = f'card1: {", ".join(child._text or "" for child in card1)}'  # pylint: disable=protected-access
            order2.text = f'card2: {", ".join(child._text or "" for child in card2)}'  # pylint: disable=protected-access
        card1.make_sortable(group='shared', on_end=handle_end_card1)
        card2.make_sortable(group='shared', on_end=lambda: ui.notify('Card2: something move_end'))

    screen.open('/')
    _drag(screen, screen.find('A'), screen.find('C'), dy=-5)
    screen.should_contain('card1: B')
    screen.should_contain('card2: A, C')
    screen.should_contain('Card1: A moved from index 0 to 0')
    screen.should_not_contain('Card2: something moved')  # because the event only fires on the source container


def test_make_sortable_twice_raises(screen: Screen):
    @ui.page('/')
    def page():
        col = ui.column()
        col.make_sortable()
        with pytest.raises(RuntimeError, match='already sortable'):
            col.make_sortable()

    screen.open('/')
