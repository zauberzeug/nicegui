from selenium.webdriver.common.by import By

from nicegui import ui

from .screen import Screen


def test_classes(screen: Screen):
    label = ui.label('Some label')

    def assert_classes(classes: str) -> None:
        assert screen.selenium.find_element(By.XPATH,
                                            f'//*[normalize-space(@class)="{classes}" and text()="Some label"]')

    screen.open('/')
    screen.wait(0.5)
    assert_classes('')

    label.classes('one')
    assert_classes('one')

    label.classes('one')
    assert_classes('one')

    label.classes('two three')
    assert_classes('one two three')

    label.classes(remove='two')
    assert_classes('one three')

    label.classes(replace='four')
    assert_classes('four')


def test_style_parsing():
    # pylint: disable=protected-access
    assert ui.element._parse_style(None) == {}  # pylint: disable=use-implicit-booleaness-not-comparison
    assert ui.element._parse_style('color: red; background-color: blue') == {'color': 'red', 'background-color': 'blue'}
    assert ui.element._parse_style('width:12em;height:34.5em') == {'width': '12em', 'height': '34.5em'}
    assert ui.element._parse_style('transform: translate(120.0px, 50%)') == {'transform': 'translate(120.0px, 50%)'}
    assert ui.element._parse_style('box-shadow: 0 0 0.5em #1976d2') == {'box-shadow': '0 0 0.5em #1976d2'}


def test_props_parsing():
    # pylint: disable=protected-access
    assert ui.element._parse_props(None) == {}  # pylint: disable=use-implicit-booleaness-not-comparison
    assert ui.element._parse_props('one two=1 three="abc def"') == {'one': True, 'two': '1', 'three': 'abc def'}
    assert ui.element._parse_props('loading percentage=12.5') == {'loading': True, 'percentage': '12.5'}
    assert ui.element._parse_props('size=50%') == {'size': '50%'}
    assert ui.element._parse_props('href=http://192.168.42.100/') == {'href': 'http://192.168.42.100/'}
    assert ui.element._parse_props('hint="Your \\"given\\" name"') == {'hint': 'Your "given" name'}
    assert ui.element._parse_props('input-style="{ color: #ff0000 }"') == {'input-style': '{ color: #ff0000 }'}


def test_style(screen: Screen):
    label = ui.label('Some label')

    def assert_style(style: str) -> None:
        assert screen.selenium.find_element(By.XPATH, f'//*[normalize-space(@style)="{style}" and text()="Some label"]')

    screen.open('/')
    screen.wait(0.5)
    assert_style('')

    label.style('color: red')
    assert_style('color: red;')

    label.style('color: red')
    assert_style('color: red;')

    label.style('color: blue')
    assert_style('color: blue;')

    label.style('font-weight: bold')
    assert_style('color: blue; font-weight: bold;')

    label.style(remove='color: blue')
    assert_style('font-weight: bold;')

    label.style(replace='text-decoration: underline')
    assert_style('text-decoration: underline;')

    label.style('color: blue;')
    assert_style('text-decoration: underline; color: blue;')


def test_props(screen: Screen):
    input_ = ui.input()

    def assert_props(*props: str) -> None:
        class_conditions = [f'contains(@class, "q-field--{prop}")' for prop in props]
        assert screen.selenium.find_element(By.XPATH, f'//label[{" and ".join(class_conditions)}]')

    screen.open('/')
    screen.wait(0.5)
    assert_props('standard')

    input_.props('dark')
    assert_props('standard', 'dark')

    input_.props('dark')
    assert_props('standard', 'dark')

    input_.props(remove='dark')
    assert_props('standard')


def test_move(screen: Screen):
    with ui.card() as a:
        ui.label('A')
        x = ui.label('X')

    with ui.card() as b:
        ui.label('B')

    ui.button('Move X to A', on_click=lambda: x.move(a))
    ui.button('Move X to B', on_click=lambda: x.move(b))
    ui.button('Move X to top', on_click=lambda: x.move(target_index=0))

    screen.open('/')
    assert screen.find('A').location['y'] < screen.find('X').location['y'] < screen.find('B').location['y']
    screen.click('Move X to B')
    screen.wait(0.5)
    assert screen.find('A').location['y'] < screen.find('B').location['y'] < screen.find('X').location['y']
    screen.click('Move X to A')
    screen.wait(0.5)
    assert screen.find('A').location['y'] < screen.find('X').location['y'] < screen.find('B').location['y']
    screen.click('Move X to top')
    screen.wait(0.5)
    assert screen.find('X').location['y'] < screen.find('A').location['y'] < screen.find('B').location['y']


def test_xss(screen: Screen):
    ui.label('</script><script>alert(1)</script>')
    ui.label('<b>Bold 1</b>, `code`, copy&paste, multi\nline')
    ui.button('Button', on_click=lambda: (
        ui.label('</script><script>alert(2)</script>'),
        ui.label('<b>Bold 2</b>, `code`, copy&paste, multi\nline'),
    ))

    screen.open('/')
    screen.click('Button')
    screen.should_contain('</script><script>alert(1)</script>')
    screen.should_contain('</script><script>alert(2)</script>')
    screen.should_contain('<b>Bold 1</b>, `code`, copy&paste, multi\nline')
    screen.should_contain('<b>Bold 2</b>, `code`, copy&paste, multi\nline')
