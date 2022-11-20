from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.element import Element

from .screen import Screen


def test_keyboard(screen: Screen):
    result = ui.label()
    ui.keyboard(on_key=lambda e: result.set_text(f'{e.key, e.action}'))

    screen.open('/')
    assert screen.selenium.find_element(By.TAG_NAME, 'base')
    assert any(s.endswith('keyboard.js') for s in screen.get_attributes('script', 'src'))

    assert screen.selenium.find_element(By.XPATH, '//span[@data-nicegui="keyboard"]')
    ActionChains(screen.selenium).send_keys('t').perform()
    screen.should_contain('t, KeyboardAction(keydown=False, keyup=True, repeat=False)')


def test_joystick(screen: Screen):
    ui.joystick(on_move=lambda e: coordinates.set_text(f'move {e.data.vector.x:.3f}, {e.data.vector.y:.3f}'),
                on_end=lambda e: coordinates.set_text('end 0, 0'))
    coordinates = ui.label('start 0, 0')

    screen.open('/')
    assert any(s.endswith('keyboard.js') for s in screen.get_attributes('script', 'src'))
    joystick = screen.selenium.find_element(By.XPATH, '//div[@data-nicegui="joystick"]')
    assert joystick
    screen.should_contain('start 0, 0')
    ActionChains(screen.selenium).move_to_element_with_offset(joystick, 25, 25)\
        .click_and_hold().pause(1).move_by_offset(20, 20).pause(1).perform()
    screen.should_contain('move 0.400, -0.400')
    ActionChains(screen.selenium).move_to_element_with_offset(joystick, 25, 25).click().perform()
    screen.should_contain('end 0, 0')


def test_styling_joystick(screen: Screen):
    ui.joystick().style('background-color: gray;').classes('shadow-lg')

    screen.open('/')
    joystick = screen.selenium.find_element(By.XPATH, '//div[@data-nicegui="joystick"]')
    assert 'background-color: gray;' in joystick.get_attribute('style')
    assert 'shadow-lg' in joystick.get_attribute('class')


def test_input_with_multi_word_error_message(screen: Screen):
    input = ui.input(label='some input')
    ui.button('set error', on_click=lambda: input.props('error error-message="Some multi word error message"'))

    screen.open('/')
    screen.should_not_contain('Some multi word error message')
    screen.click('set error')
    screen.should_contain('Some multi word error message')


def test_classes(screen: Screen):
    label = ui.label('Some label')

    def assert_classes(classes: str) -> None:
        assert screen.selenium.find_element(By.XPATH,
                                            f'//*[normalize-space(@class)="{classes}" and text()="Some label"]')

    screen.open('/')
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
    assert Element._parse_style('color: red; background-color: green') == {'color': 'red', 'background-color': 'green'}
    assert Element._parse_style('width:12em;height:34.5em') == {'width': '12em', 'height': '34.5em'}
    assert Element._parse_style('transform: translate(120.0px, 50%)') == {'transform': 'translate(120.0px, 50%)'}
    assert Element._parse_style('box-shadow: 0 0 0.5em #1976d2') == {'box-shadow': '0 0 0.5em #1976d2'}


def test_props_parsing():
    assert Element._parse_props('one two=1 three="abc def"') == {'one': True, 'two': '1', 'three': 'abc def'}
    assert Element._parse_props('loading percentage=12.5') == {'loading': True, 'percentage': '12.5'}
    assert Element._parse_props('size=50%') == {'size': '50%'}


def test_style(screen: Screen):
    label = ui.label('Some label')

    def assert_style(style: str) -> None:
        assert screen.selenium.find_element(By.XPATH, f'//*[normalize-space(@style)="{style}" and text()="Some label"]')

    screen.open('/')
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
    input = ui.input()

    def assert_props(*props: str) -> None:
        class_conditions = [f'contains(@class, "q-field--{prop}")' for prop in props]
        assert screen.selenium.find_element(By.XPATH, f'//label[{" and ".join(class_conditions)}]')

    screen.open('/')
    assert_props('standard', 'labeled')

    input.props('dark')
    assert_props('standard', 'labeled', 'dark')

    input.props('dark')
    assert_props('standard', 'labeled', 'dark')

    input.props(remove='dark')
    assert_props('standard', 'labeled')


def test_adding_toggle_options(screen: Screen):
    label = ui.label()
    toggle = ui.toggle(['A', 'B', 'C'], on_change=lambda e: label.set_text(f'Choice: {e.value}'))

    def add_option():
        toggle.options.append('D')
        toggle.update()

    ui.button('Add option', on_click=add_option)

    screen.open('/')
    screen.click('A')
    screen.should_contain('Choice: A')

    screen.should_not_contain('D')
    screen.click('Add option')
    screen.should_contain('D')
    screen.click('D')
    screen.should_contain('Choice: D')


def test_base64_image(screen: Screen):
    ui.image('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABmJLR0QA/wD/AP+gvaeTAAAEHElEQVRoge2ZXUxbZRjHf6enH3QtBQ7paIFlMO2AMXTGqZE40bCpiRdzF06Nsu3O6G68MH5MnYkk3vhx4cWCJppFlvgZ74wXbsZdLCYaQMeWUWM30EJZgVM+WtpS2uNFoQzTU3pKu2O0v8v38//Pe57ned8cKFOmTBk9EVR7vrxsRlJ6gR7AfdMUrWcC6EcWTnK4fSnbAKPqVEl5C3ipRMLypR54GUkBeCXbAEOOyUdKoahAjqp15DKg12eTDZdaRy4DN43p+1s55HTwVF0Vk/taNM3V3UCDxUStSWQ4HKPDXsFwOK5pvm4GTILADquZbslGPKUAsNdRwXg8wQ6rOe911NPo2UvKplXmYOcWM957Par9wrnL6xv2786qVbcT8EUTSOdH+Co4T//kLE0XfgfgwcFRpPMjea+jm4GkohBaTuKxmhlaiNFoMZFS4Jf5KKHlZN7rqBeyEvPF7kYO11UBsKdyLUuGH2jjNV+Qt0en8lpHtxN41RfkyUt+APYPjfJNcJ7v5TB7f77KJxOhvNfRzcDVaPpqM51Ick6O4DQbuTC7yMBClMml5bzX0bUOdNgtXAzHAGi3WRiOaKsBoGMa1cy/LY0Wi7IBvfl/GhCAJ+qq+HbPdgL7Whi8+5YN59zjsOLr9ODr9PB6s7OQbbOiuRI7jAa+7tjGAcmeaQtukLdNgsBHbfWZW2atSdS6rSqaDAjAp7saOSDZSSoKpwOznJmcw7uYO3+/uL2W2+wVm9GpiiYD3ZKNg85KAI57A3w4vnHJv9Vq5o1mJ9FUCqMgYBLUS08haIqBY+4aAK5E4lyJxDnV4ub0rgaOuasRswgTgL7WeqwGA73XpjIPl2Ki6QQ6q6wAbDUb+fHO5kwZP+qu5qDTwaGLf64bf8RdTbdkYzgc492xGU40FS94V9F0Ai5L2q9kEunzyxz3BhhYiALwmLOSh24IbKfZyHseFykFnh0JkFBKczPRZMBqSA//eCLE894Ap/wyDw+NsZhMAWTiA+B9Tx21JpG+cZmf5haLKHk9mgysCp1bTmXaZhJJvIvpq3HTSpq83V7BM65qAHrc1chdrchdrdjE9HbPNUjIXa2bV49GA6tC22yWTJsoCLhXPq3ZRHKlbW1OpWigxihSYxQzMWMxCNQYi1MLNAXxZ9fnuKOygkckO0+7qjgrR3hhWy0uc3qZ72bCAPwWjmd9mPvv28kW0UDfuMyJP4JFkK/RwAd/zfD4Vgd3OaycaW9c1/dDKMLn1+eAtQf7P1kN41gqe38haPqE4imF7sFR3hmbZiyWIKEo+KJL9F6b4tFfx1jeINMMLcQYWIjijyU2JfpG/tMvsokSSSkAYVytJ5eB/hIoKQxBUdWiHsSycHLlz0gP6T8lepD+xTQjvKnT/mXKlCmzAX8Dl7JCqRHaepQAAAAASUVORK5CYII=').style('width: 50px;')

    screen.open('/')
    screen.wait(0.2)
    image = screen.selenium.find_element(By.CLASS_NAME, 'q-img__image')
    assert 'background-image: url("data:image/png;base64,iVB' in image.get_attribute('style')
