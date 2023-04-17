from nicegui import ui

from .screen import Screen


def test_local_target_linking_on_sub_pages(screen: Screen):
    '''The issue arose when using <base> tag for reverse-proxy path handling. See https://github.com/zauberzeug/nicegui/pull/188#issuecomment-1336313925'''
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


def test_replacing_link(screen: Screen):
    def change():
        content.clear()
        with content:
            ui.link('zauberzeug', 'https://zauberzeug.com')
    with ui.row() as content:
        ui.link('nicegui.io', 'https://nicegui.io')
    ui.button('change link', on_click=change)

    screen.open('/')
    content.clear()
    screen.should_not_contain('nicegui')
    screen.click('change link')
    assert screen.find('zauberzeug').get_attribute('href') == 'https://zauberzeug.com/'
