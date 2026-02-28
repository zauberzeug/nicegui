from nicegui import ui
from nicegui.js_action import JsAction, has_js_action, js_action
from nicegui.testing import Screen


def test_dialog_open_close_with_js_action(screen: Screen):
    """Test that on_click=dialog.open/close works with the js_action decorator."""
    @ui.page('/')
    def page():
        with ui.dialog() as d, ui.card():
            ui.label('Dialog Content')
            ui.button('Close', on_click=d.close)
        ui.button('Open', on_click=d.open)

    screen.open('/')
    screen.should_not_contain('Dialog Content')

    screen.click('Open')
    screen.wait(0.5)
    screen.should_contain('Dialog Content')

    screen.click('Close')
    screen.wait(0.5)
    screen.should_not_contain('Dialog Content')


def test_dialog_open_close_direct_call(screen: Screen):
    """Test that dialog.open() and dialog.close() still work as direct method calls."""
    @ui.page('/')
    def page():
        with ui.dialog() as d, ui.card():
            ui.label('Dialog Content')
            ui.button('Close', on_click=lambda: d.close())
        ui.button('Open', on_click=lambda: d.open())

    screen.open('/')
    screen.should_not_contain('Dialog Content')

    screen.click('Open')
    screen.wait(0.5)
    screen.should_contain('Dialog Content')

    screen.click('Close')
    screen.wait(0.5)
    screen.should_not_contain('Dialog Content')


def test_menu_open_close_with_js_action(screen: Screen):
    """Test that on_click=menu.open/close works with the js_action decorator."""
    @ui.page('/')
    def page():
        with ui.button('Menu'):
            with ui.menu() as menu:
                ui.menu_item('Item 1')
        ui.button('Open Menu', on_click=menu.open)
        ui.label().bind_text_from(menu, 'value', lambda v: 'menu open' if v else 'menu closed')

    screen.open('/')
    screen.should_contain('menu closed')

    screen.click('Open Menu')
    screen.wait(0.5)
    screen.should_contain('menu open')
    screen.should_contain('Item 1')


def test_fab_open_close_toggle_with_js_action(screen: Screen):
    """Test that on_click=fab.open/close/toggle works with the js_action decorator."""
    @ui.page('/')
    def page():
        with ui.fab('menu', label='FAB') as fab:
            ui.fab_action('info', label='Action 1')
        ui.button('Open', on_click=fab.open)
        ui.button('Close', on_click=fab.close)
        ui.button('Toggle', on_click=fab.toggle)
        ui.label().bind_text_from(fab, 'value', lambda v: 'FAB open' if v else 'FAB closed')

    screen.open('/')
    screen.should_contain('FAB closed')

    screen.click('Open')
    screen.wait(0.5)
    screen.should_contain('FAB open')

    screen.click('Close')
    screen.wait(0.5)
    screen.should_contain('FAB closed')

    screen.click('Toggle')
    screen.wait(0.5)
    screen.should_contain('FAB open')

    screen.click('Toggle')
    screen.wait(0.5)
    screen.should_contain('FAB closed')


def test_js_handler_is_installed_on_event_listener(screen: Screen):
    """Test that passing a js_action-decorated method installs a JS handler on the listener."""
    @ui.page('/')
    def page():
        with ui.dialog() as d, ui.card():
            ui.label('Content')
        button = ui.button('Open', on_click=d.open)
        # Verify the event listener has a js_handler set
        listeners = list(button._event_listeners.values())
        click_listeners = [el for el in listeners if el.type == 'click']
        assert len(click_listeners) == 1
        assert click_listeners[0].js_handler is not None
        assert 'model-value' in click_listeners[0].js_handler
        assert 'invalidateVnodeCache' in click_listeners[0].js_handler

    screen.open('/')


def test_has_js_action_detects_decorated_methods(screen: Screen):
    """Test that has_js_action correctly identifies decorated bound methods."""
    @ui.page('/')
    def page():
        dialog = ui.dialog()
        menu = ui.menu()

        # Decorated bound methods should be detected
        assert has_js_action(dialog.open)
        assert has_js_action(dialog.close)
        assert has_js_action(menu.open)
        assert has_js_action(menu.close)
        assert has_js_action(menu.toggle)

        # Regular callables should not be detected
        assert not has_js_action(lambda: None)
        assert not has_js_action(print)

        # JsAction instances should be detected
        action = JsAction(dialog, lambda: None, '() => {}')
        assert has_js_action(action)

    screen.open('/')


def test_js_action_decorator_preserves_method_behavior(screen: Screen):
    """Test that @js_action decorator does not alter normal method behavior."""
    @ui.page('/')
    def page():
        dialog = ui.dialog()
        assert dialog.value is False

        dialog.open()
        assert dialog.value is True

        dialog.close()
        assert dialog.value is False

    screen.open('/')


def test_dialog_await_still_works(screen: Screen):
    """Test that the dialog __await__ protocol still works with js_action methods."""
    @ui.page('/')
    def page():
        with ui.dialog() as dialog, ui.card():
            ui.button('Yes', on_click=lambda: dialog.submit('Yes'))

        async def show() -> None:
            ui.notify(f'Result: {await dialog}')

        ui.button('Open', on_click=show)

    screen.open('/')
    screen.click('Open')
    screen.wait(0.5)
    screen.click('Yes')
    screen.should_contain('Result: Yes')


def test_subclass_can_override_js_action_method(screen: Screen):
    """Test that subclasses can override js_action-decorated methods."""
    class MyDialog(ui.dialog):
        def __init__(self):
            super().__init__()
            self.open_count = 0

        def open(self):
            self.open_count += 1
            super().open()

    @ui.page('/')
    def page():
        d = MyDialog()
        with d, ui.card():
            ui.label('Content')
        ui.button('Open', on_click=d.open)  # bare bound method: should NOT get js_action treatment
        ui.label().bind_text_from(d, 'open_count', lambda c: f'Opened {c} times')
        assert not has_js_action(d.open)

    screen.open('/')
    screen.click('Open')
    screen.wait(0.5)
    screen.should_contain('Content')
    screen.should_contain('Opened 1 times')


def test_dropdown_button_open_close_toggle(screen: Screen):
    """Test that DropdownButton open/close/toggle work with js_action."""
    @ui.page('/')
    def page():
        with ui.dropdown_button('Dropdown') as dd:
            ui.item('Option A')
        ui.button('Open', on_click=dd.open)
        ui.button('Close', on_click=dd.close)
        ui.button('Toggle', on_click=dd.toggle)
        ui.label().bind_text_from(dd, 'value', lambda v: 'DD open' if v else 'DD closed')

    screen.open('/')
    screen.should_contain('DD closed')

    screen.click('Open')
    screen.wait(0.5)
    screen.should_contain('DD open')

    screen.click('Close')
    screen.wait(0.5)
    screen.should_contain('DD closed')

    screen.click('Toggle')
    screen.wait(0.5)
    screen.should_contain('DD open')


def test_menu_item_auto_close_uses_js_action(screen: Screen):
    """Test that MenuItem auto_close works with the js_action on Menu.close."""
    @ui.page('/')
    def page():
        with ui.button('Open'):
            with ui.menu() as menu:
                ui.menu_item('Click me', on_click=lambda: ui.notify('clicked'))
        ui.label().bind_text_from(menu, 'value', lambda v: 'menu open' if v else 'menu closed')

    screen.open('/')
    screen.click('Open')
    screen.wait(0.5)
    screen.should_contain('menu open')

    screen.click('Click me')
    screen.wait(0.5)
    screen.should_contain('clicked')
    screen.should_contain('menu closed')


def test_custom_js_action_decorator(screen: Screen):
    """Test that users can create their own js_action-decorated methods."""
    class MyElement(ui.element):
        def __init__(self):
            super().__init__('div')
            self._count = 0

        @js_action(lambda self: '(...args) => { emit(...args); }')
        def increment(self):
            self._count += 1

    @ui.page('/')
    def page():
        el = MyElement()
        assert has_js_action(el.increment)
        el.increment()
        assert el._count == 1
        ui.label('OK')

    screen.open('/')
    screen.should_contain('OK')
