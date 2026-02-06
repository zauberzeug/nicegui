from nicegui import ui
from nicegui.testing import SharedScreen


def test_notification(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.button('Notify', on_click=lambda: ui.notification('Hi!'))

    shared_screen.open('/')
    shared_screen.click('Notify')
    shared_screen.should_contain('Hi!')


def test_close_button(shared_screen: SharedScreen):
    b = None

    @ui.page('/')
    def page():
        nonlocal b
        b = ui.button('Notify', on_click=lambda: ui.notification('Hi!', timeout=None, close_button=True))

    shared_screen.open('/')
    shared_screen.click('Notify')
    shared_screen.should_contain('Hi!')
    assert len(b.client.layout.default_slot.children) == 2
    shared_screen.wait_for('Close')
    shared_screen.wait(0.1)  # NOTE: wait for button to become clickable
    shared_screen.click('Close')
    shared_screen.wait(1.5)
    shared_screen.should_not_contain('Hi!')
    assert len(b.client.layout.default_slot.children) == 1


def test_dismiss(shared_screen: SharedScreen):
    n = None
    b = None

    @ui.page('/')
    def page():
        nonlocal n, b
        n = ui.notification('Hi!', timeout=None)
        b = ui.button('Dismiss', on_click=n.dismiss)

    shared_screen.open('/')
    shared_screen.should_contain('Hi!')
    assert len(b.client.layout.default_slot.children) == 2
    shared_screen.wait(1)
    shared_screen.click('Dismiss')
    shared_screen.wait(1.5)
    shared_screen.should_not_contain('Hi!')
    assert len(b.client.layout.default_slot.children) == 1


def test_no_reset_by_other_notifications(shared_screen: SharedScreen):
    # see #4373
    @ui.page('/')
    def page():
        ui.button('Button A', on_click=lambda: ui.notification('Notification A', timeout=1.0))
        ui.button('Button B', on_click=lambda: ui.notification('Notification B', timeout=1.0))
        ui.button('Button C', on_click=lambda: ui.notification('Notification C', timeout=1.0))
        ui.button('Button D', on_click=lambda: ui.notification('Notification D', timeout=1.0))

    shared_screen.open('/')
    shared_screen.click('Button A')
    shared_screen.wait(1)
    shared_screen.click('Button B')
    shared_screen.wait(1)
    shared_screen.click('Button C')
    shared_screen.wait(1)
    shared_screen.click('Button D')
    shared_screen.should_contain('Notification D')
    shared_screen.should_not_contain('Notification A')
