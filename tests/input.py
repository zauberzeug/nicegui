from nicegui import ui

from .screen import Screen


def test_input_with_multi_word_error_message(screen: Screen):
    input = ui.input(label='some input')
    ui.button('set error', on_click=lambda: input.props('error error-message="Some multi word error message"'))

    screen.open('/')
    screen.should_not_contain('Some multi word error message')

    screen.click('set error')
    screen.should_contain('Some multi word error message')
