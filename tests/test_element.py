import pytest
from selenium.webdriver.common.by import By

from nicegui import background_tasks, ui
from nicegui.testing import Screen


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
    assert ui.element._parse_props('accept=.jpeg,.jpg,.png') == {'accept': '.jpeg,.jpg,.png'}

    assert ui.element._parse_props('empty=""') == {'empty': ''}
    assert ui.element._parse_props("empty=''") == {'empty': ''}

    assert ui.element._parse_props("""hint='Your \\"given\\" name'""") == {'hint': 'Your "given" name'}
    assert ui.element._parse_props("one two=1 three='abc def'") == {'one': True, 'two': '1', 'three': 'abc def'}
    assert ui.element._parse_props('''three='abc def' four="hhh jjj"''') == {'three': 'abc def', 'four': 'hhh jjj', }
    assert ui.element._parse_props('''foo="quote'quote"''') == {'foo': "quote'quote"}
    assert ui.element._parse_props("""foo='quote"quote'""") == {'foo': 'quote"quote'}
    assert ui.element._parse_props("""foo="single '" bar='double "'""") == {'foo': "single '", 'bar': 'double "'}
    assert ui.element._parse_props("""foo="single '" bar='double \\"'""") == {'foo': "single '", 'bar': 'double "'}
    assert ui.element._parse_props("input-style='{ color: #ff0000 }'") == {'input-style': '{ color: #ff0000 }'}
    assert ui.element._parse_props("""input-style='{ myquote: "quote" }'""") == {'input-style': '{ myquote: "quote" }'}
    assert ui.element._parse_props('filename=foo=bar.txt') == {'filename': 'foo=bar.txt'}


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


def test_default_props():
    ui.button.default_props('rounded outline')
    button_a = ui.button('Button A')
    button_b = ui.button('Button B')
    assert button_a._props.get('rounded') is True, 'default props are set'
    assert button_a._props.get('outline') is True
    assert button_b._props.get('rounded') is True
    assert button_b._props.get('outline') is True

    ui.button.default_props(remove='outline')
    button_c = ui.button('Button C')
    assert button_c._props.get('outline') is None, '"outline" prop was removed'
    assert button_c._props.get('rounded') is True, 'other props are still there'

    ui.input.default_props('filled')
    input_a = ui.input()
    assert input_a._props.get('filled') is True
    assert input_a._props.get('rounded') is None, 'default props of ui.button do not affect ui.input'

    class MyButton(ui.button):
        pass
    MyButton.default_props('flat')
    button_d = MyButton()
    button_e = ui.button()
    assert button_d._props.get('flat') is True
    assert button_d._props.get('rounded') is True, 'default props are inherited'
    assert button_e._props.get('flat') is None, 'default props of MyButton do not affect ui.button'
    assert button_e._props.get('rounded') is True

    ui.button.default_props('no-caps').default_props('no-wrap')
    button_f = ui.button()
    assert button_f._props.get('no-caps') is True
    assert button_f._props.get('no-wrap') is True


def test_default_classes():
    ui.button.default_classes('bg-white text-green')
    button_a = ui.button('Button A')
    button_b = ui.button('Button B')
    assert 'bg-white' in button_a._classes, 'default classes are set'
    assert 'text-green' in button_a._classes
    assert 'bg-white' in button_b._classes
    assert 'text-green' in button_b._classes

    ui.button.default_classes(remove='text-green')
    button_c = ui.button('Button C')
    assert 'text-green' not in button_c._classes, '"text-green" class was removed'
    assert 'bg-white' in button_c._classes, 'other classes are still there'

    ui.input.default_classes('text-black')
    input_a = ui.input()
    assert 'text-black' in input_a._classes
    assert 'bg-white' not in input_a._classes, 'default classes of ui.button do not affect ui.input'

    class MyButton(ui.button):
        pass
    MyButton.default_classes('w-full')
    button_d = MyButton()
    button_e = ui.button()
    assert 'w-full' in button_d._classes
    assert 'bg-white' in button_d._classes, 'default classes are inherited'
    assert 'w-full' not in button_e._classes, 'default classes of MyButton do not affect ui.button'
    assert 'bg-white' in button_e._classes

    ui.button.default_classes('h-40').default_classes('max-h-80')
    button_f = ui.button()
    assert 'h-40' in button_f._classes
    assert 'max-h-80' in button_f._classes


def test_default_style():
    ui.button.default_style('color: green; font-size: 200%')
    button_a = ui.button('Button A')
    button_b = ui.button('Button B')
    assert button_a._style.get('color') == 'green', 'default style is set'
    assert button_a._style.get('font-size') == '200%'
    assert button_b._style.get('color') == 'green'
    assert button_b._style.get('font-size') == '200%'

    ui.button.default_style(remove='color: green')
    button_c = ui.button('Button C')
    assert button_c._style.get('color') is None, '"color" style was removed'
    assert button_c._style.get('font-size') == '200%', 'other style are still there'

    ui.input.default_style('font-weight: 300')
    input_a = ui.input()
    assert input_a._style.get('font-weight') == '300'
    assert input_a._style.get('font-size') is None, 'default style of ui.button does not affect ui.input'

    class MyButton(ui.button):
        pass
    MyButton.default_style('font-family: courier')
    button_d = MyButton()
    button_e = ui.button()
    assert button_d._style.get('font-family') == 'courier'
    assert button_d._style.get('font-size') == '200%', 'default style is inherited'
    assert button_e._style.get('font-family') is None, 'default style of MyButton does not affect ui.button'
    assert button_e._style.get('font-size') == '200%'

    ui.button.default_style('border: 2px').default_style('padding: 30px')
    button_f = ui.button()
    assert button_f._style.get('border') == '2px'
    assert button_f._style.get('padding') == '30px'


def test_invalid_tags(screen: Screen):
    good_tags = ['div', 'div-1', 'DIV', 'däv', 'div_x', '🙂']
    bad_tags = ['<div>', 'hi hi', 'hi/ho', 'foo$bar']
    for tag in good_tags:
        ui.element(tag)
    for tag in bad_tags:
        with pytest.raises(ValueError):
            ui.element(tag)

    screen.open('/')


def test_bad_characters(screen: Screen):
    ui.label(r'& <test> ` ${foo}')

    screen.open('/')
    screen.should_contain(r'& <test> ` ${foo}')


def test_update_before_client_connection(screen: Screen):
    @ui.page('/')
    def page():
        label = ui.label('Hello world!')

        async def update():
            label.text = 'Hello again!'
        background_tasks.create(update())

    screen.open('/')
    screen.should_contain('Hello again!')
