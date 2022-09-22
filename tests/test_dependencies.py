from nicegui import ui

from .user import User


def test_joystick_dependency(user: User):
    @ui.page('/')
    def page():
        ui.joystick()

    user.open('/')
    srcs = user.get_attributes('script', 'src')
    assert any(s.endswith('joystick.js') for s in srcs)
    assert any(s.endswith('nipplejs.min.js') for s in srcs)
    user.sleep(2)  # NOTE we need to sleep here so the js timeout error is printed (start pytest with -s to see it)


def test_keyboard_dependency_before_startup(user: User):
    @ui.page('/')
    def page():
        ui.keyboard()

    user.open('/')
    assert any(s.endswith('keyboard.js') for s in user.get_attributes('script', 'src'))
    user.sleep(2)  # NOTE we need to sleep here so the js timeout error is printed (start pytest with -s to see it)


def test_keyboard_dependency_after_startup(user: User):
    @ui.page('/')
    def page():
        ui.button('activate keyboard', on_click=lambda: ui.keyboard())

    user.open('/')
    assert not any(s.endswith('keyboard.js') for s in user.get_attributes('script', 'src'))
    user.click('activate keyboard')
    assert any(s.endswith('keyboard.js') for s in user.get_attributes('script', 'src'))
    user.sleep(2)  # NOTE we need to sleep here so the js timeout error is printed (start pytest with -s to see it)
