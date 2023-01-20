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
