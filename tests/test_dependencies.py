from nicegui import ui

from .user import User


def test_joystick_dependency(user: User):
    @ui.page('/')
    def page():
        ui.joystick()

    user.open('/')
    sources = user.get_attributes('script', 'src')
    assert any(s.endswith('joystick.js') for s in sources)
    assert any(s.endswith('nipplejs.min.js') for s in sources)


def test_keyboard_dependency_before_startup(user: User):
    @ui.page('/')
    def page():
        ui.keyboard()

    user.open('/')
    assert any(s.endswith('keyboard.js') for s in user.get_attributes('script', 'src'))


def test_keyboard_dependency_after_startup(user: User):
    @ui.page('/')
    def page():
        def add_keyboard():
            with row:
                ui.keyboard()
        row = ui.row()
        ui.button('activate keyboard', on_click=add_keyboard)

    user.open('/')
    assert not any(s.endswith('keyboard.js') for s in user.get_attributes('script', 'src'))
    user.click('activate keyboard')
    assert any(s.endswith('keyboard.js') for s in user.get_attributes('script', 'src'))
