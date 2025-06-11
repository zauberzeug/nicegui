from nicegui import ui
from nicegui.testing import Screen


def test_local_target_linking_on_sub_pages(screen: Screen):
    """The issue arose when using <base> tag for reverse-proxy path handling. See https://github.com/zauberzeug/nicegui/pull/188#issuecomment-1336313925"""
    @ui.page('/sub')
    def main():
        ui.link('goto target', '#target').style('margin-bottom: 600px')
        ui.link_target('target')
        ui.label('the target')

    ui.label('main page')

    screen.open('/sub')
    screen.click('goto target')
    screen.should_contain('the target')
    screen.should_not_contain('main page')


def test_opening_link_in_new_tab(screen: Screen):
    @ui.page('/sub')
    def subpage():
        ui.label('the sub-page')

    ui.link('open sub-page in new tab', '/sub', new_tab=True)

    screen.open('/')
    screen.click('open sub-page')
    screen.switch_to(1)
    screen.should_contain('the sub-page')
    screen.should_not_contain('open sub-page')
    screen.switch_to(0)
    screen.should_not_contain('the sub-page')
    screen.should_contain('open sub-page')


def test_replace_link(screen: Screen):
    with ui.row() as container:
        ui.link('nicegui.io', 'https://nicegui.io/')

    def replace():
        container.clear()
        with container:
            ui.link('zauberzeug', 'https://zauberzeug.com/')
    ui.button('Replace', on_click=replace)

    screen.open('/')
    assert screen.find('nicegui.io').get_attribute('href') == 'https://nicegui.io/'
    screen.click('Replace')
    assert screen.find('zauberzeug').get_attribute('href') == 'https://zauberzeug.com/'


def test_updating_href_prop(screen: Screen):
    label = ui.link('nicegui.io', 'https://nicegui.io')
    ui.button('change href', on_click=lambda: label.props('href="https://github.com/zauberzeug/nicegui"'))

    screen.open('/')
    assert screen.find('nicegui.io').get_attribute('href') == 'https://nicegui.io/'
    screen.click('change href')
    assert screen.find('nicegui.io').get_attribute('href') == 'https://github.com/zauberzeug/nicegui'


def test_link_to_elements(screen: Screen):
    navigation = ui.row()
    for i in range(100):
        ui.label(f'label {i}')
    link = ui.link('goto top', navigation)
    with navigation:
        ui.link('goto bottom', link)

    screen.open('/')
    assert screen.selenium.execute_script('return window.scrollY') == 0
    screen.click('goto bottom')
    screen.wait(0.5)
    assert screen.selenium.execute_script('return window.scrollY') > 100
    screen.click('goto top')
    screen.wait(0.5)
    assert screen.selenium.execute_script('return window.scrollY') < 100
