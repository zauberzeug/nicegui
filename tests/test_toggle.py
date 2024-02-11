from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_adding_toggle_options(screen: SeleniumScreen):
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


def test_changing_options(screen: SeleniumScreen):
    t = ui.toggle([10, 20, 30], value=10)
    ui.label().bind_text_from(t, 'value', lambda v: f'value = {v}')
    ui.button('reverse', on_click=lambda: (t.options.reverse(), t.update()))
    ui.button('clear', on_click=lambda: (t.options.clear(), t.update()))

    screen.open('/')
    screen.click('reverse')
    screen.should_contain('value = 10')
    screen.click('clear')
    screen.should_contain('value = None')


def test_clearable_toggle(screen: SeleniumScreen):
    t = ui.toggle(['A', 'B', 'C'], clearable=True)
    ui.label().bind_text_from(t, 'value', lambda v: f'value = {v}')

    screen.open('/')
    screen.click('A')
    screen.should_contain('value = A')

    screen.click('A')
    screen.should_contain('value = None')
