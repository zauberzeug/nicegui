from nicegui import ui
from nicegui.testing import Screen


def test_adding_toggle_options(screen: Screen):
    @ui.page('/')
    def page():
        label = ui.label()
        options = [ui.as_option(v) for v in ('A', 'B', 'C')]
        toggle = ui.toggle(options, on_change=lambda e: label.set_text(f'Choice: {tuple(o.label for o in e.value)}'))

        def add_option():
            toggle.options.append(ui.as_option('D'))
            toggle.update()

        ui.button('Add option', on_click=add_option)

    screen.open('/')
    screen.click('A')
    screen.should_contain("Choice: ('A',)")
    screen.should_not_contain('D')

    screen.click('Add option')
    screen.should_contain('D')

    screen.click('D')
    screen.should_contain("Choice: ('D',)")


def test_changing_options(screen: Screen):
    @ui.page('/')
    def page():
        options = [ui.as_option(v) for v in (10, 20, 30)]
        t = ui.toggle(options, value=(options[0],))
        ui.label().bind_text_from(t, 'value', lambda v: f'value = {tuple(o.label for o in v)}')
        ui.button('reverse', on_click=lambda: (t.options.reverse(), t.update()))
        ui.button('clear', on_click=lambda: (t.options.clear(), t.update()))

    screen.open('/')
    screen.click('reverse')
    screen.should_contain('value = (10,)')

    screen.click('clear')
    screen.should_contain('value = ()')


def test_clearable_toggle(screen: Screen):
    @ui.page('/')
    def page():
        t = ui.toggle([ui.as_option(v) for v in ('A', 'B', 'C')], clearable=True)
        ui.label().bind_text_from(t, 'value', lambda v: f'value = {tuple(o.label for o in v)}')

    screen.open('/')
    screen.click('A')
    screen.should_contain("value = ('A',)")

    screen.click('A')
    screen.should_contain('value = ()')
