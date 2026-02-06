from nicegui import ui
from nicegui.testing import SharedScreen


def test_adding_toggle_options(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        label = ui.label()
        toggle = ui.toggle(['A', 'B', 'C'], on_change=lambda e: label.set_text(f'Choice: {e.value}'))

        def add_option():
            toggle.options.append('D')
            toggle.update()

        ui.button('Add option', on_click=add_option)

    shared_screen.open('/')
    shared_screen.click('A')
    shared_screen.should_contain('Choice: A')
    shared_screen.should_not_contain('D')

    shared_screen.click('Add option')
    shared_screen.should_contain('D')

    shared_screen.click('D')
    shared_screen.should_contain('Choice: D')


def test_changing_options(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        t = ui.toggle([10, 20, 30], value=10)
        ui.label().bind_text_from(t, 'value', lambda v: f'value = {v}')
        ui.button('reverse', on_click=lambda: (t.options.reverse(), t.update()))
        ui.button('clear', on_click=lambda: (t.options.clear(), t.update()))

    shared_screen.open('/')
    shared_screen.click('reverse')
    shared_screen.should_contain('value = 10')

    shared_screen.click('clear')
    shared_screen.should_contain('value = None')


def test_clearable_toggle(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        t = ui.toggle(['A', 'B', 'C'], clearable=True)
        ui.label().bind_text_from(t, 'value', lambda v: f'value = {v}')

    shared_screen.open('/')
    shared_screen.click('A')
    shared_screen.should_contain('value = A')

    shared_screen.click('A')
    shared_screen.should_contain('value = None')
