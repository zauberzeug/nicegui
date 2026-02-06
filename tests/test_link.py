from nicegui import ui
from nicegui.testing import SharedScreen


def test_local_target_linking_on_sub_pages(shared_screen: SharedScreen):
    """The issue arose when using <base> tag for reverse-proxy path handling. See https://github.com/zauberzeug/nicegui/pull/188#issuecomment-1336313925"""
    @ui.page('/sub')
    def main():
        ui.link('goto target', '#target').style('margin-bottom: 600px')
        ui.link_target('target')
        ui.label('the target')

    @ui.page('/')
    def page():
        ui.label('main page')

    shared_screen.open('/sub')
    shared_screen.click('goto target')
    shared_screen.should_contain('the target')
    shared_screen.should_not_contain('main page')


def test_opening_link_in_new_tab(shared_screen: SharedScreen):
    @ui.page('/sub')
    def subpage():
        ui.label('the sub-page')

    @ui.page('/')
    def page():
        ui.link('open sub-page in new tab', '/sub', new_tab=True)

    shared_screen.open('/')
    shared_screen.click('open sub-page')
    shared_screen.switch_to(1)
    shared_screen.should_contain('the sub-page')
    shared_screen.should_not_contain('open sub-page')
    shared_screen.switch_to(0)
    shared_screen.should_not_contain('the sub-page')
    shared_screen.should_contain('open sub-page')


def test_replace_link(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.row() as container:
            ui.link('nicegui.io', 'https://nicegui.io/')

        def replace():
            with container.clear():
                ui.link('zauberzeug', 'https://zauberzeug.com/')
        ui.button('Replace', on_click=replace)

    shared_screen.open('/')
    assert shared_screen.find('nicegui.io').get_attribute('href') == 'https://nicegui.io/'

    shared_screen.click('Replace')
    assert shared_screen.find('zauberzeug').get_attribute('href') == 'https://zauberzeug.com/'


def test_updating_href_prop(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        link = ui.link('nicegui.io', 'https://nicegui.io')
        ui.button('change href', on_click=lambda: (
            link.props('href="https://github.com/zauberzeug/nicegui"'),
            ui.notify('href changed'),
        ))

    shared_screen.open('/')
    assert shared_screen.find('nicegui.io').get_attribute('href') == 'https://nicegui.io/'

    shared_screen.click('change href')
    shared_screen.should_contain('href changed')
    assert shared_screen.find('nicegui.io').get_attribute('href') == 'https://github.com/zauberzeug/nicegui'


def test_link_to_elements(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        navigation = ui.row()
        for i in range(100):
            ui.label(f'label {i}')
        link = ui.link('goto top', navigation)
        with navigation:
            ui.link('goto bottom', link)

    shared_screen.open('/')
    assert shared_screen.selenium.execute_script('return window.scrollY') == 0

    shared_screen.click('goto bottom')
    shared_screen.wait(0.5)
    assert shared_screen.selenium.execute_script('return window.scrollY') > 100

    shared_screen.click('goto top')
    shared_screen.wait(0.5)
    assert shared_screen.selenium.execute_script('return window.scrollY') < 100
