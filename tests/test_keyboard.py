from nicegui import ui
from nicegui.testing import Screen


def test_keyboard(screen: Screen):
    @ui.page('/')
    def page():
        result = ui.label()
        ui.keyboard(on_key=lambda e: result.set_text(f'{e.key, e.action}'))

    screen.open('/')
    screen.wait(1.0)
    screen.type('t')
    screen.should_contain('t, KeyboardAction(keydown=False, keyup=True, repeat=False)')


def test_keyboard_removes_listeners_on_unmount(screen: Screen):
    @ui.page('/')
    def page():
        ui.add_head_html('''
            <script>
                window.__kd = 0;
                const _add = document.addEventListener.bind(document);
                const _rem = document.removeEventListener.bind(document);
                document.addEventListener = function(type) {
                    if (type === 'keydown') window.__kd++;
                    return _add.apply(document, arguments);
                };
                document.removeEventListener = function(type) {
                    if (type === 'keydown') window.__kd--;
                    return _rem.apply(document, arguments);
                };
            </script>
        ''')
        show = {'on': True}

        @ui.refreshable
        def keyboard():
            if show['on']:
                ui.keyboard()

        keyboard()
        ui.button('toggle', on_click=lambda: (show.update(on=not show['on']), keyboard.refresh()))

    screen.open('/')
    screen.wait(0.5)
    for _ in range(3):
        screen.click('toggle')
        screen.wait(0.2)
        screen.click('toggle')
        screen.wait(0.2)
    screen.click('toggle')
    screen.wait(0.5)
    assert screen.selenium.execute_script('return window.__kd') == 0
