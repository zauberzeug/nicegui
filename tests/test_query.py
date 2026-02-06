from nicegui import ui
from nicegui.testing import SharedScreen


def test_query_body(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.label('Hello')
        ui.query('body').classes('bg-orange-100')
        ui.button('Red background', on_click=lambda: ui.query('body').classes(replace='bg-red-100'))
        ui.button('Blue background', on_click=lambda: ui.query('body').classes(replace='bg-blue-100'))
        ui.button('Small padding', on_click=lambda: ui.query('body').style('padding: 1px'))
        ui.button('Large padding', on_click=lambda: ui.query('body').style('padding: 10px'))
        ui.button('Data X = 1', on_click=lambda: ui.query('body').props('data-x=1'))
        ui.button('Data X = 2', on_click=lambda: ui.query('body').props('data-x=2'))

    def get_bg_classes() -> list[str]:
        return [c for c in (shared_screen.find_by_tag('body').get_attribute('class') or '').split() if c.startswith('bg-')]

    shared_screen.open('/')
    shared_screen.should_contain('Hello')
    assert get_bg_classes() == ['bg-orange-100']

    shared_screen.click('Red background')
    shared_screen.wait(0.5)
    assert get_bg_classes() == ['bg-red-100']

    shared_screen.click('Blue background')
    shared_screen.wait(0.5)
    assert get_bg_classes() == ['bg-blue-100']

    shared_screen.click('Small padding')
    shared_screen.wait(0.5)
    assert shared_screen.find_by_tag('body').value_of_css_property('padding') == '1px'

    shared_screen.click('Large padding')
    shared_screen.wait(0.5)
    assert shared_screen.find_by_tag('body').value_of_css_property('padding') == '10px'

    shared_screen.click('Data X = 1')
    shared_screen.wait(0.5)
    assert shared_screen.find_by_tag('body').get_attribute('data-x') == '1'

    shared_screen.click('Data X = 2')
    shared_screen.wait(0.5)
    assert shared_screen.find_by_tag('body').get_attribute('data-x') == '2'


def test_query_multiple_divs(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.label('A')
        ui.label('B')
        ui.button('Add border', on_click=lambda: ui.query('div').style('border: 1px solid black'))

    shared_screen.open('/')
    shared_screen.click('Add border')
    shared_screen.wait(0.5)
    assert shared_screen.find('A').value_of_css_property('border') == '1px solid rgb(0, 0, 0)'
    assert shared_screen.find('B').value_of_css_property('border') == '1px solid rgb(0, 0, 0)'


def test_query_with_css_variables(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.add_body_html('<div id="element">Test</div>')
        ui.query('#element').style('--color: red; color: var(--color)')

    shared_screen.open('/')
    assert shared_screen.find('Test').value_of_css_property('color') == 'rgba(255, 0, 0, 1)'
