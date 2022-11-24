from nicegui import ui

from .screen import Screen


def test_adding_toggle_options(screen: Screen):
    label = ui.label()
    toggle = ui.toggle(['A', 'B', 'C'], on_change=lambda e: label.set_text(f'Choice: {e.value}'))

    def add_option():
        toggle.options.append('D')
        toggle.update()

    ui.button('Add option', on_click=add_option)

    screen.open('/')
    screen.click('A')
    screen.should_contain('Choice: A')

    screen.should_not_contain('D')
    screen.click('Add option')
    screen.should_contain('D')
    screen.click('D')
    screen.should_contain('Choice: D')
