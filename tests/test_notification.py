from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_notification(screen: SeleniumScreen):
    ui.button('Notify', on_click=lambda: ui.notification('Hi!'))

    screen.open('/')
    screen.click('Notify')
    screen.should_contain('Hi!')


def test_close_button(screen: SeleniumScreen):
    b = ui.button('Notify', on_click=lambda: ui.notification('Hi!', timeout=None, close_button=True))

    screen.open('/')
    screen.click('Notify')
    screen.should_contain('Hi!')
    assert len(b.client.layout.default_slot.children) == 2
    screen.click('Close')
    screen.wait(1.5)
    screen.should_not_contain('Hi!')
    assert len(b.client.layout.default_slot.children) == 1


def test_dismiss(screen: SeleniumScreen):
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
