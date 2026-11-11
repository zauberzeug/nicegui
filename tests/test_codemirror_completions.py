import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.testing import Screen


def _rendered_labels(screen: Screen) -> list[str]:
    return screen.selenium.execute_script(
        'return Array.from(document.querySelectorAll(".cm-tooltip-autocomplete .cm-completionLabel"))'
        '.map(e => e.textContent);'
    )


def _open_count(screen: Screen) -> int:
    return screen.selenium.execute_script(
        'return document.querySelectorAll(".cm-tooltip-autocomplete li").length'
    )


def test_completions_basic(screen: Screen):
    @ui.page('/')
    def page():
        ui.codemirror('', completions=[
            {'label': 'foo_bar', 'detail': 'a function', 'type': 'function', 'boost': 1,
             'class_name': 'cm-foo'},
            {'label': 'foo_baz', 'display_label': 'foo_baz (preferred)', 'type': 'function', 'boost': 99},
            {'label': 'qux', 'type': 'variable'},
        ])

    screen.open('/')
    cm = screen.selenium.find_element(By.XPATH, '//*[contains(@class, "cm-content")]')
    cm.click()
    cm.send_keys('foo')
    screen.wait_for(lambda: _open_count(screen) == 2)
    rendered = _rendered_labels(screen)
    assert 'qux' not in rendered
    assert rendered[0] == 'foo_baz (preferred)'
    assert rendered[1] == 'foo_bar'
    has_class = screen.selenium.execute_script(
        'return Array.from(document.querySelectorAll(".cm-tooltip-autocomplete li"))'
        '.some(li => li.classList.contains("cm-foo"));'
    )
    assert has_class


def test_set_completions_replaces(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('', completions=[{'label': 'banana'}])

    screen.open('/')
    cm = screen.selenium.find_element(By.XPATH, '//*[contains(@class, "cm-content")]')
    editor.completions = [{'label': 'bar'}, {'label': 'baz'}]
    # Wait for the new completions to land on the client before opening the
    # popup — otherwise typing can race the websocket flush and trigger the
    # autocomplete against the stale [banana] source.
    screen.wait_for(lambda: screen.selenium.execute_script(
        f'return getElement({editor.id})?.completions?.length === 2'
    ))
    cm.click()
    cm.send_keys('ba')
    screen.wait_for(lambda: _open_count(screen) == 2)
    rendered = _rendered_labels(screen)
    assert sorted(rendered) == ['bar', 'baz']  # banana is gone


@pytest.mark.parametrize('replace, expect_print', [(False, True), (True, False)])
def test_replace_language_completions(screen: Screen, replace: bool, expect_print: bool):
    @ui.page('/')
    def page():
        ui.codemirror('', language='Python',
                      completions=[{'label': 'rbt.move', 'type': 'function'}],
                      replace_language_completions=replace)

    screen.open('/')
    cm = screen.selenium.find_element(By.XPATH, '//*[contains(@class, "cm-content")]')
    cm.click()
    cm.send_keys('print')
    if expect_print:
        screen.wait_for(lambda: 'print' in _rendered_labels(screen))
    else:
        # Replace-mode + a non-matching prefix should produce no popup. Wait briefly
        # for the autocomplete machinery to settle, then assert nothing rendered.
        screen.wait(0.5)
        assert 'print' not in _rendered_labels(screen)


def test_complete_words_in_document(screen: Screen):
    @ui.page('/')
    def page():
        ui.codemirror('apple banana cherry\n', complete_words_in_document=True)

    screen.open('/')
    cm = screen.selenium.find_element(By.XPATH, '//*[contains(@class, "cm-content")]')
    cm.click()
    cm.send_keys(Keys.END)
    cm.send_keys('app')
    screen.wait_for(lambda: 'apple' in _rendered_labels(screen))


def test_snippet_completion(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('', completions=[
            {'label': 'mysnippet', 'snippet': True,
             'apply': 'for ${1:item} in ${2:iterable}:\n    ${3:pass}'},
        ])

    screen.open('/')
    cm = screen.selenium.find_element(By.XPATH, '//*[contains(@class, "cm-content")]')
    cm.click()
    editor.trigger_completion()
    screen.wait_for(lambda: 'mysnippet' in _rendered_labels(screen))
    # CM6 first-option auto-selection is set on a microtask after the popup mounts; CI runners
    # are slow enough that ENTER can race ahead of `selected: 0` being committed, in which case
    # the keystroke falls through to a newline insert instead of accepting the completion.
    screen.wait_for(lambda: screen.selenium.execute_script(
        'return !!document.querySelector(\'.cm-tooltip-autocomplete li[aria-selected="true"]\')'
    ))
    cm.send_keys(Keys.ENTER)
    screen.wait_for(lambda: 'for item in iterable:' in (editor.value or ''))
    assert 'pass' in editor.value


def test_tooltip_class(screen: Screen):
    @ui.page('/')
    def page():
        ui.codemirror('', completions=[{'label': 'foo'}], tooltip_class='cm-popup-wide')

    screen.open('/')
    cm = screen.selenium.find_element(By.XPATH, '//*[contains(@class, "cm-content")]')
    cm.click()
    cm.send_keys('f')
    screen.wait_for(lambda: screen.selenium.execute_script(
        'return !!document.querySelector(".cm-tooltip-autocomplete.cm-popup-wide");'
    ))


def test_trigger_completion(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('', completions=[{'label': 'hello'}])

    screen.open('/')
    cm = screen.selenium.find_element(By.XPATH, '//*[contains(@class, "cm-content")]')
    cm.click()
    editor.trigger_completion()
    screen.wait_for(lambda: 'hello' in _rendered_labels(screen))


def test_completion_info_default_is_plain_text(screen: Screen):
    @ui.page('/')
    def page():
        ui.codemirror('', completions=[
            {'label': 'foo', 'info': '<b>raw</b>'},
        ])

    screen.open('/')
    cm = screen.selenium.find_element(By.XPATH, '//*[contains(@class, "cm-content")]')
    cm.click()
    cm.send_keys('foo')
    screen.wait_for(lambda: _open_count(screen) == 1)
    screen.wait_for(lambda: screen.selenium.execute_script(
        'const tip = document.querySelector(".cm-completionInfo");'
        'return !!(tip && tip.textContent.includes("<b>raw</b>"));'
    ))
    has_bold = screen.selenium.execute_script(
        'const tip = document.querySelector(".cm-completionInfo");'
        'return !!(tip && tip.querySelector("b"));'
    )
    assert not has_bold, 'default rendering must not interpret HTML'


def test_completion_info_html_opt_in_renders_sanitized(screen: Screen):
    @ui.page('/')
    def page():
        ui.codemirror('', completion_info_html=True, completions=[
            {'label': 'foo',
             'info': '<b>safe</b><script>window.__info_hijack=1</script>'},
        ])

    screen.open('/')
    cm = screen.selenium.find_element(By.XPATH, '//*[contains(@class, "cm-content")]')
    cm.click()
    cm.send_keys('foo')
    screen.wait_for(lambda: _open_count(screen) == 1)
    # Trigger info-tooltip rendering by selecting the option (default selection on a single match).
    screen.wait_for(lambda: screen.selenium.execute_script(
        'const tip = document.querySelector(".cm-completionInfo");'
        'return !!(tip && tip.querySelector("b"));'
    ))
    has_script = screen.selenium.execute_script(
        'const tip = document.querySelector(".cm-completionInfo");'
        'return !!(tip && tip.querySelector("script"));'
    )
    hijacked = screen.selenium.execute_script('return window.__info_hijack === 1')
    assert not has_script, 'DOMPurify should have stripped <script>'
    assert not hijacked, 'inline script must not have executed'
