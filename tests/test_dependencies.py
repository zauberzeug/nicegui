import pytest
from nicegui import ui
from selenium.common.exceptions import NoSuchElementException

from .user import User


def test_keyboard_before_startup(user: User):
    @ui.page('/')
    def page():
        ui.keyboard()

    user.open('/')
    assert any(s.endswith('keyboard.js') for s in user.get_attributes('script', 'src'))
    assert user.selenium.find_element_by_tag_name('span')


def test_keyboard_after_startup(user: User):
    @ui.page('/')
    def page():
        def add_keyboard():
            with row:
                ui.keyboard()
        row = ui.row()
        ui.button('activate keyboard', on_click=add_keyboard)

    user.open('/')
    assert not any(s.endswith('keyboard.js') for s in user.get_attributes('script', 'src'))
    with pytest.raises(NoSuchElementException):
        user.selenium.find_element_by_tag_name('span')
    user.click('activate keyboard')
    assert any(s.endswith('keyboard.js') for s in user.get_attributes('script', 'src'))
    user.sleep(1)
    assert user.selenium.find_element_by_tag_name('span')  # FIXME: ptw fails (which is correct) while pytest does not
