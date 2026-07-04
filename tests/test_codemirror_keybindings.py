import json
import re

import pytest
from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.testing import Screen


def _press(screen: Screen, key: str, *, ctrl: bool = False) -> None:
    args = {
        'key': key,
        'code': f'Key{key.upper()}' if len(key) == 1 else key,
        'ctrlKey': ctrl,
        'bubbles': True,
        'cancelable': True,
    }
    screen.selenium.execute_script(f'''
        document.querySelector(".cm-content").dispatchEvent(new KeyboardEvent("keydown", {json.dumps(args)}));
    ''')


def test_map_and_unmap_callbacks(screen: Screen):
    @ui.page('/')
    def page():
        editor = ui.codemirror('hello', keymap={
            'Ctrl-s': lambda: ui.notify('saved'),
            'F5': lambda: ui.notify('refreshed'),
        })
        ui.button('Map X', on_click=lambda: editor.map_key('x', lambda: ui.notify('X pressed')))
        ui.button('Re-map X', on_click=lambda: editor.map_key('x', lambda: ui.notify('X typed')))
        ui.button('Unmap X', on_click=lambda: editor.unmap_key('x'))

    screen.open('/')
    screen.should_contain('hello')

    _press(screen, 's', ctrl=True)
    screen.should_contain('saved')

    _press(screen, 'F5')
    screen.should_contain('refreshed')

    screen.click('Map X')
    screen.wait_for(lambda: (_press(screen, 'x'), 'X pressed' in screen.selenium.page_source)[1])

    screen.click('Re-map X')
    screen.wait_for(lambda: (_press(screen, 'x'), 'X typed' in screen.selenium.page_source)[1])

    screen.click('Unmap X')
    screen.click('hello')  # focus the editor
    screen.wait_for(lambda: (screen.type(Keys.END + 'x'), 'hellox' in screen.selenium.page_source)[1])


@pytest.mark.parametrize('prevent_default', [True, False])
def test_prevent_default_controls_default_input(screen: Screen, prevent_default: bool):
    @ui.page('/')
    def page():
        editor = ui.codemirror('hell', keymap={
            'o': ui.codemirror.KeyBinding(lambda: ui.notify('fired'), prevent_default=prevent_default),
        })
        ui.label().bind_text_from(editor, 'value', lambda value: f'<{value}>')

    screen.open('/')
    screen.click('hell')
    screen.type(Keys.END + 'o')
    screen.should_contain('fired')
    screen.should_contain('<hell>' if prevent_default else '<hello>')


def test_keymap_does_not_fire_while_disabled(screen: Screen):
    events: list[str] = []

    @ui.page('/')
    def page():
        editor = ui.codemirror('hello', keymap={
            'x': lambda e: events.append(f'fired while {"enabled" if e.sender.enabled else "disabled"}'),
        })
        ui.button('Disable', on_click=editor.disable)
        ui.button('Enable', on_click=editor.enable)
        ui.label().bind_text_from(editor, 'enabled', lambda value: f'enabled={value}')

    screen.open('/')
    screen.should_contain('hello')

    _press(screen, 'x')
    screen.wait_for(lambda: events == ['fired while enabled'])

    screen.click('Disable')
    screen.should_contain('enabled=False')
    _press(screen, 'x')  # must not fire while disabled

    screen.click('Enable')
    screen.should_contain('enabled=True')
    _press(screen, 'x')
    screen.wait_for(lambda: events == ['fired while enabled'] * 2)


@pytest.mark.parametrize('keybinding, error', [
    pytest.param('Ctr-s', 'Unrecognized modifier name', id='bad-modifier'),  # 'Ctr' is not a valid modifier
    pytest.param('Mod-a Mod-b', 'used both as a regular binding and as a multi-stroke prefix', id='prefix-conflict'),
])
def test_invalid_keybinding_is_reported(screen: Screen, keybinding: str, error: str):
    @ui.page('/')
    def page():
        ui.codemirror('hello', keymap={keybinding: lambda: None})

    screen.allowed_js_errors.append(error)
    screen.open('/')
    screen.should_contain('hello')
    screen.wait_for(lambda: any(error in record.message for record in screen.caplog.records))
    screen.assert_py_logger('ERROR', re.compile(error))
