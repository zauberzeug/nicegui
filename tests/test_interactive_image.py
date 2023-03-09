from nicegui import Client, ui

from .screen import Screen


def test_set_source_in_tab(screen: Screen):
    """https://github.com/zauberzeug/nicegui/issues/488"""
    @ui.page('/')
    async def page(client: Client):
        with ui.tabs() as tabs:
            ui.tab('A')
            ui.tab('B')
        with ui.tab_panels(tabs, value='A'):
            with ui.tab_panel('A'):
                ui.label('Tab A')
                img = ui.interactive_image()
            with ui.tab_panel('B'):
                ui.label('Tab B')
        await client.connected()
        img.set_source('https://nicegui.io/logo.png')

    screen.open('/')
    screen.wait(0.5)
    assert screen.find_by_tag('img').get_attribute('src') == 'https://nicegui.io/logo.png'
    screen.click('B')
    screen.wait(0.5)
    screen.click('A')
    assert screen.find_by_tag('img').get_attribute('src') == 'https://nicegui.io/logo.png'
