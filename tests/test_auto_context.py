from nicegui import ui

from .user import User


def test_adding_element_to_index_page(user: User):
    ui.button('add label', on_click=lambda: ui.label('added'))

    user.open('/')
    user.click('add label')
    user.should_see('added')


def test_adding_element_to_private_page(user: User):
    @ui.page('/')
    def page():
        ui.button('add label', on_click=lambda: ui.label('added'))

    user.open('/')
    user.click('add label')
    user.should_see('added')
