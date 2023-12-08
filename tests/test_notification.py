from nicegui import ui

from .screen import Screen


def test_notification(screen: Screen):
    b = ui.button('Notify', on_click=lambda: ui.notification('Hi!', timeout=1.0))

    screen.open('/')
    screen.click('Notify')
    screen.should_contain('Hi!')
    assert len(b.client.layout.default_slot.children) == 2
    screen.wait(1.5)
    assert len(b.client.layout.default_slot.children) == 1


def test_close_button(screen: Screen):
    b = ui.button('Notify', on_click=lambda: ui.notification('Hi!', timeout=None, close_button=True))

    screen.open('/')
    screen.click('Notify')
    screen.should_contain('Hi!')
    assert len(b.client.layout.default_slot.children) == 2
    screen.click('Close')
    screen.wait(1.5)
    screen.should_not_contain('Hi!')
    assert len(b.client.layout.default_slot.children) == 1
