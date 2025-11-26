from nicegui import ui
from nicegui.testing import Screen

COLOR_CASES = [
    ('1', 'rgba(239, 83, 80, 1)', 'red-5'),
    ('2', 'oklch(0.637 0.237 25.331)', 'red-500'),
    ('3', 'rgba(255, 0, 0, 1)', '#ff0000'),
    ('4', 'rgba(0, 255, 255, 1)', '#00ffff'),
]


def test_quasar_colors(screen: Screen):
    @ui.page('/')
    def page():
        ui.button()
        ui.button(color=None)
        for _, _, color in COLOR_CASES:
            ui.button(color=color)

    screen.open('/')
    assert screen.find_all_by_tag('button')[0].value_of_css_property('background-color') == 'rgba(88, 152, 212, 1)'
    assert screen.find_all_by_tag('button')[1].value_of_css_property('background-color') == 'rgba(0, 0, 0, 0)'
    for i, (_, expected_color, _) in enumerate(COLOR_CASES, start=2):
        assert screen.find_all_by_tag('button')[i].value_of_css_property('background-color') == expected_color


def test_quasar_colors_via_setter(screen: Screen):
    @ui.page('/')
    def page():
        mybutton = ui.button()
        display = ui.label()
        mybutton.bind_background_color_to(display, 'text', forward=lambda c: f'###{c}###')
        for label, _, color in COLOR_CASES:
            ui.button(label, on_click=lambda c=color: mybutton.set_background_color(c))

    screen.open('/')

    assert screen.find_all_by_tag('button')[0].value_of_css_property('background-color') == 'rgba(88, 152, 212, 1)'

    for label, expected_color, color in COLOR_CASES:
        screen.click(label)
        screen.wait(1)
        assert screen.find_all_by_tag('button')[0].value_of_css_property('background-color') == expected_color
        screen.should_contain(f'###{color}###')


def test_quasar_colors_via_binding(screen: Screen):
    @ui.page('/')
    def page():
        mybutton = ui.button()
        mytoggle = ui.toggle({color: f'Choice {label}' for label, _, color in COLOR_CASES}, value='red-5')
        mybutton.bind_background_color_from(mytoggle, 'value')

    screen.open('/')

    for label, expected_color, _ in COLOR_CASES:
        screen.click(f'Choice {label}')
        screen.wait(1)
        assert screen.find_all_by_tag('button')[0].value_of_css_property('background-color') == expected_color


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
