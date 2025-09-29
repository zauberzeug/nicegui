from nicegui import ui
from nicegui.testing import Screen


def test_quasar_colors(screen: Screen):
    @ui.page('/')
    def page():
        ui.button()
        ui.button(color=None)
        ui.button(color='red-5')
        ui.button(color='red-500')
        ui.button(color='#ff0000')
        ui.button().classes('!bg-[#00ffff]')

    screen.open('/')
    assert screen.find_all_by_tag('button')[0].value_of_css_property('background-color') == 'rgba(88, 152, 212, 1)'
    assert screen.find_all_by_tag('button')[1].value_of_css_property('background-color') == 'rgba(0, 0, 0, 0)'
    assert screen.find_all_by_tag('button')[2].value_of_css_property('background-color') == 'rgba(239, 83, 80, 1)'
    assert screen.find_all_by_tag('button')[3].value_of_css_property('background-color') == 'oklch(0.637 0.237 25.331)'
    assert screen.find_all_by_tag('button')[4].value_of_css_property('background-color') == 'rgba(255, 0, 0, 1)'
    assert screen.find_all_by_tag('button')[5].value_of_css_property('background-color') == 'rgba(0, 255, 255, 1)'


def test_enable_disable(screen: Screen):
    events = []

    @ui.page('/')
    def page():
        b = ui.button('Button', on_click=lambda: events.append(1))
        ui.button('Enable', on_click=b.enable)
        ui.button('Disable', on_click=b.disable)

    screen.open('/')
    screen.click('Button')
    assert events == [1]

    screen.click('Disable')
    screen.click('Button')
    assert events == [1]

    screen.click('Enable')
    screen.click('Button')
    assert events == [1, 1]
