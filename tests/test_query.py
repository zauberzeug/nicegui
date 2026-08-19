from nicegui import ui
from nicegui.testing import Screen


def test_query_body(screen: Screen):
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
        return [c for c in (screen.find_by_tag('body').get_attribute('class') or '').split() if c.startswith('bg-')]

    screen.open('/')
    screen.should_contain('Hello')
    assert get_bg_classes() == ['bg-orange-100']

    screen.click('Red background')
    screen.wait(0.5)
    assert get_bg_classes() == ['bg-red-100']

    screen.click('Blue background')
    screen.wait(0.5)
    assert get_bg_classes() == ['bg-blue-100']

    screen.click('Small padding')
    screen.wait(0.5)
    assert screen.find_by_tag('body').value_of_css_property('padding') == '1px'

    screen.click('Large padding')
    screen.wait(0.5)
    assert screen.find_by_tag('body').value_of_css_property('padding') == '10px'

    screen.click('Data X = 1')
    screen.wait(0.5)
    assert screen.find_by_tag('body').get_attribute('data-x') == '1'

    screen.click('Data X = 2')
    screen.wait(0.5)
    assert screen.find_by_tag('body').get_attribute('data-x') == '2'


def test_query_multiple_divs(screen: Screen):
    @ui.page('/')
    def page():
        ui.label('A')
        ui.label('B')
        ui.button('Add border', on_click=lambda: ui.query('div').style('border: 1px solid black'))

    screen.open('/')
    screen.click('Add border')
    screen.wait(0.5)
    assert screen.find('A').value_of_css_property('border') == '1px solid rgb(0, 0, 0)'
    assert screen.find('B').value_of_css_property('border') == '1px solid rgb(0, 0, 0)'


def test_query_style_replace(screen: Screen):
    @ui.page('/')
    def page():
        ui.label('Hello')
        ui.query('body').style('color: rgb(255, 0, 0); font-size: 20px')
        ui.button('Replace', on_click=lambda: ui.query('body').style(replace='font-size: 30px'))

    screen.open('/')
    screen.should_contain('Hello')
    assert screen.find_by_tag('body').value_of_css_property('font-size') == '20px'
    assert '255, 0, 0' in screen.find_by_tag('body').value_of_css_property('color')

    screen.click('Replace')
    screen.wait_for(lambda: screen.find_by_tag('body').value_of_css_property('font-size') == '30px')
    assert '255, 0, 0' not in screen.find_by_tag('body').value_of_css_property('color')


def test_query_remove_foreign_style_and_classes(screen: Screen):
    @ui.page('/')
    def page():
        ui.add_body_html('<div id="banner" class="foo bar" style="color: rgb(255, 0, 0)">Banner</div>')
        ui.button('Remove', on_click=lambda: ui.query('#banner').classes(remove='foo').style(remove='color: red'))

    screen.open('/')
    assert screen.find('Banner').get_attribute('class') == 'foo bar'
    assert '255, 0, 0' in screen.find('Banner').value_of_css_property('color')

    screen.click('Remove')
    screen.wait_for(lambda: screen.find('Banner').get_attribute('class') == 'bar')
    screen.wait_for(lambda: '255, 0, 0' not in screen.find('Banner').value_of_css_property('color'))


def test_query_with_css_variables(screen: Screen):
    @ui.page('/')
    def page():
        ui.add_body_html('<div id="element">Test</div>')
        ui.query('#element').style('--color: red; color: var(--color)')

    screen.open('/')
    assert screen.find('Test').value_of_css_property('color') == 'rgba(255, 0, 0, 1)'
