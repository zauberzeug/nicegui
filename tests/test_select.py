from nicegui import ui

from .screen import Screen


def test_select(screen: Screen):
    ui.select(['A', 'B', 'C'], value='A')

    screen.open('/')
    screen.should_contain('A')
    screen.should_not_contain('B')
    screen.should_not_contain('C')

    screen.click('A')  # open the dropdown
    screen.click('B')  # close the dropdown
    screen.wait(0.5)
    screen.should_not_contain('A')
    screen.should_contain('B')
    screen.should_not_contain('C')


def test_select_with_input(screen: Screen):
    ui.select(['A', 'AB', 'XYZ'], with_input=True)

    screen.open('/')
    screen.find_by_tag('input').click()
    screen.should_contain('XYZ')

    screen.find_by_tag('input').send_keys('A')
    screen.wait(0.5)
    screen.should_contain('A')
    screen.should_contain('AB')
    screen.should_not_contain('XYZ')


def test_replace_select(screen: Screen):
    with ui.row() as container:
        ui.select(['A'], value='A')

    def replace():
        container.clear()
        with container:
            ui.select(['B'], value='B')
    ui.button('Replace', on_click=replace)

    screen.open('/')
    screen.should_contain('A')
    screen.click('Replace')
    screen.should_contain('B')
    screen.should_not_contain('A')
