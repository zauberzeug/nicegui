from nicegui import ui
from nicegui.testing import Screen


def test_notification(screen: Screen):
    ui.button('Notify', on_click=lambda: ui.notification('Hi!'))

    screen.open('/')
    screen.click('Notify')
    screen.should_contain('Hi!')


def test_close_button(screen: Screen):
    b = ui.button('Notify', on_click=lambda: ui.notification('Hi!', timeout=None, close_button=True))

    screen.open('/')
    screen.click('Notify')
    screen.should_contain('Hi!')
    assert len(b.client.layout.default_slot.children) == 2
    screen.wait_for('Close')
    screen.wait(0.1)  # NOTE: wait for button to become clickable
    screen.click('Close')
    screen.wait(1.5)
    screen.should_not_contain('Hi!')
    assert len(b.client.layout.default_slot.children) == 1


def test_dismiss(screen: Screen):
    n = ui.notification('Hi!', timeout=None)
    b = ui.button('Dismiss', on_click=n.dismiss)

    screen.open('/')
    screen.should_contain('Hi!')
    assert len(b.client.layout.default_slot.children) == 2
    screen.wait(1)
    screen.click('Dismiss')
    screen.wait(1.5)
    screen.should_not_contain('Hi!')
    assert len(b.client.layout.default_slot.children) == 1
