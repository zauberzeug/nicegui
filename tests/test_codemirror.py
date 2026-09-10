import re
from typing import Any

import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.testing import Screen, User

# pylint: disable=protected-access


def test_codemirror(screen: Screen):
    @ui.page('/')
    def page():
        ui.codemirror('Line 1\nLine 2\nLine 3')

    screen.open('/')
    screen.should_contain('Line 2')


def test_supported_values(screen: Screen):
    values: dict[str, list[str]] = {}

    @ui.page('/')
    def page():
        editor = ui.codemirror()

        async def fetch():
            values['languages'] = await editor.run_method('getLanguages')
            values['themes'] = await editor.run_method('getThemes')
            values['supported_themes'] = editor.supported_themes
            values['supported_languages'] = editor.supported_languages
            ui.label('Done')
        ui.button('Fetch', on_click=fetch)

    screen.open('/')
    screen.click('Fetch')
    screen.wait_for('Done')
    assert values['languages'] == values['supported_languages']
    assert values['themes'] == values['supported_themes']


@pytest.mark.parametrize('doc, sections, inserted, expected', [
    ('', [0, 1], [['A']], 'A'),
    ('', [0, 2], [['AB']], 'AB'),
    ('X', [1, 2], [['AB']], 'AB'),
    ('X', [1, -1], [], 'X'),
    ('X', [1, -1, 0, 1], [[], ['Y']], 'XY'),
    ('Hello', [5, -1, 0, 8], [[], [', world!']], 'Hello, world!'),
    ('Hello, world!', [5, -1, 7, 0, 1, -1], [], 'Hello!'),
    ('Hello, hello!', [2, -1, 3, 1, 4, -1, 3, 1, 1, -1], [[], ['y'], [], ['y']], 'Hey, hey!'),
    ('Hello, world!', [5, -1, 1, 3, 7, -1], [[], [' 🙂']], 'Hello 🙂 world!'),
    ('Hey! 🙂', [7, -1, 0, 4], [[], [' Ho!']], 'Hey! 🙂 Ho!'),
    ('Ha 🙂\nha 🙂', [3, -1, 2, 0, 4, -1, 2, 0], [[], [''], [], ['']], 'Ha \nha '),
])
def test_change_set(screen: Screen, doc: str, sections: list[int], inserted: list[list[str]], expected: str):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror(doc)

    screen.open('/')
    assert editor._apply_change_set(sections, inserted) == expected


def test_set_value_preserves_cursor(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('Hello World')

    screen.open('/')
    cm = screen.selenium.find_element(By.XPATH, '//*[contains(@class, "cm-content")]')
    cm.click()
    cm.send_keys(Keys.HOME)
    for _ in range(5):
        cm.send_keys(Keys.ARROW_RIGHT)  # Move cursor after 'Hello'

    editor.value = 'Hello Earth'
    screen.wait(0.5)

    cm.send_keys(',')  # Insert comma after 'Hello'
    screen.wait(0.5)

    assert editor.value == 'Hello, Earth'


def test_encode_codepoints():
    assert ui.codemirror._encode_codepoints('') == b''
    assert ui.codemirror._encode_codepoints('Hello') == bytes([1, 1, 1, 1, 1])
    assert ui.codemirror._encode_codepoints('🙂') == bytes([0, 1])
    assert ui.codemirror._encode_codepoints('Hello 🙂') == bytes([1, 1, 1, 1, 1, 1, 0, 1])
    assert ui.codemirror._encode_codepoints('😎😎😎') == bytes([0, 1, 0, 1, 0, 1])


def test_set_and_clear_line_decorations(screen: Screen):
    editor = _open_editor(screen, 'alpha\nbeta\ngamma\ndelta')
    editor.decorations = [
        {'kind': 'line', 'line': 1, 'class': 'my-line-class'},
        {'kind': 'line', 'line': 3, 'class': 'my-line-class'},
    ]
    screen.wait_for(lambda: _line_decoration_count(screen, 'my-line-class') == 2)
    editor.decorations = []
    screen.wait_for(lambda: _line_decoration_count(screen, 'my-line-class') == 0)


def test_decorations_list_mutations_sync(screen: Screen):
    editor = _open_editor(screen, 'one\ntwo\nthree')
    editor.decorations.append({'kind': 'line', 'line': 1, 'class': 'set-a'})
    editor.decorations.append({'kind': 'line', 'line': 2, 'class': 'set-b'})
    screen.wait_for(lambda: _line_decoration_count(screen, 'set-a') == 1
                    and _line_decoration_count(screen, 'set-b') == 1)
    del editor.decorations[0]
    screen.wait_for(lambda: _line_decoration_count(screen, 'set-a') == 0
                    and _line_decoration_count(screen, 'set-b') == 1)
    editor.decorations.clear()
    screen.wait_for(lambda: _line_decoration_count(screen, 'set-b') == 0)


def test_replace_decoration_collapses_range(screen: Screen):
    editor = _open_editor(screen)
    baseline = _visible_text_length(screen)
    # 'beta\n' spans offsets 6..11 (5 chars + newline) — collapse hides those characters.
    editor.decorations = [{'kind': 'replace', 'from': 6, 'to': 11}]
    screen.wait_for(lambda: _visible_text_length(screen) < baseline)
    editor.decorations = []
    screen.wait_for(lambda: _visible_text_length(screen) == baseline)


def test_replace_decoration_with_text(screen: Screen):
    editor = _open_editor(screen)
    editor.decorations = [
        {'kind': 'replace', 'from': 6, 'to': 10, 'text': 'BETA-NEW', 'class': 'cm-test-suggest'},
    ]
    screen.wait_for(lambda: _span_count(screen, 'cm-test-suggest') == 1)
    widget_text = _marked_text(screen, 'cm-test-suggest')
    assert widget_text == 'BETA-NEW'
    # Document is unchanged — the editor's value must still contain the original text.
    assert 'beta' in editor.value
    assert 'BETA-NEW' not in editor.value


def test_widget_text_renders_html_sanitized(screen: Screen):
    editor = _open_editor(screen, decoration_text_html=True)
    editor.decorations = [
        {'kind': 'widget', 'position': 5,
         'text': '<b onclick="window.hijacked = true">safe</b><script>window.hijacked = true</script>',
         'class': 'cm-test-html-widget'},
    ]
    screen.wait_for(lambda: screen.selenium.execute_script(
        'const w = document.querySelector(".cm-content span.cm-test-html-widget");'
        'return !!(w && w.querySelector("b"));'
    ))
    # Assert on the sanitized DOM rather than on a "did it run" flag: scripts inserted via innerHTML
    # never execute, so such a flag stays unset even without sanitization. Dropping the sanitizer
    # leaves both the script element and the handler attribute in place, which is what we check.
    sanitized = screen.selenium.execute_script(
        'const w = document.querySelector(".cm-content span.cm-test-html-widget");'
        'return {script: !!w.querySelector("script"), handler: !!w.querySelector("[onclick]")};'
    )
    assert not sanitized['script'], 'DOMPurify strips <script> elements'
    assert not sanitized['handler'], 'DOMPurify strips inline event handlers'


def test_widget_text_defaults_to_plain(screen: Screen):
    editor = _open_editor(screen)
    editor.decorations = [
        {'kind': 'widget', 'position': 5,
         'text': '<b>literal</b>',
         'class': 'cm-test-plain-widget'},
    ]
    screen.wait_for(lambda: _span_count(screen, 'cm-test-plain-widget') == 1)
    widget_html = screen.selenium.execute_script(
        'return document.querySelector(".cm-content span.cm-test-plain-widget").innerHTML;'
    )
    widget_text = _marked_text(screen, 'cm-test-plain-widget')
    assert '<b>' not in widget_html, 'plain mode must render < and > as entities'
    assert widget_text == '<b>literal</b>'


def test_replace_decoration_block_mode(screen: Screen):
    editor = _open_editor(screen, 'alpha\nbeta\ngamma\ndelta')
    # Lines 2-3 ('beta\ngamma') span offsets 6..16 — must cover full lines for block mode.
    editor.decorations = [{
        'kind': 'replace', 'from': 6, 'to': 16,
        'text': '{ ... folded ... }', 'class': 'cm-test-fold', 'block': True,
    }]
    screen.wait_for(lambda: _span_count(screen, 'cm-test-fold') == 1)
    visible = screen.selenium.execute_script(
        'return document.querySelector(".cm-content").innerText;'
    )
    assert 'beta' not in visible
    assert 'gamma' not in visible
    assert '{ ... folded ... }' in visible


def test_mark_decoration_styles_range(screen: Screen):
    editor = _open_editor(screen)
    editor.decorations = [{
        'kind': 'mark', 'from': 6, 'to': 10,
        'class': 'cm-test-mark', 'attributes': {'data-marker': 'beta'},
    }]
    screen.wait_for(lambda: _span_count(screen, 'cm-test-mark') == 1)
    marker_attr = screen.selenium.execute_script(
        'return document.querySelector(".cm-content span.cm-test-mark").getAttribute("data-marker");'
    )
    assert marker_attr == 'beta'
    assert editor.value == 'alpha\nbeta\ngamma'
    editor.decorations = []
    screen.wait_for(lambda: _span_count(screen, 'cm-test-mark') == 0)


def test_widget_decoration_inserts_text(screen: Screen):
    editor = _open_editor(screen)
    editor.decorations = [
        {'kind': 'widget', 'position': 5, 'text': '<-- end of alpha', 'class': 'cm-test-hint'},
    ]
    screen.wait_for(lambda: _span_count(screen, 'cm-test-hint') == 1)
    widget_text = _marked_text(screen, 'cm-test-hint')
    assert widget_text == '<-- end of alpha'
    # Document is unchanged — widgets are presentation only.
    assert editor.value == 'alpha\nbeta\ngamma'


def test_invalid_decoration_specs_skipped_not_fatal(screen: Screen):
    editor = _open_editor(screen)
    # A spec that only the document can refute — a line past its end — is skipped with a warning
    # rather than throwing and voiding the whole batch or silently retargeting another line.
    # Structural mistakes never reach the browser; they raise at the assignment site instead.
    editor.decorations = [
        {'kind': 'line', 'line': 9999, 'class': 'out-of-range'},
        {'kind': 'line', 'line': 2, 'class': 'valid'},
    ]
    screen.wait_for(lambda: _line_decoration_count(screen, 'valid') == 1)
    assert _line_decoration_count(screen, 'out-of-range') == 0


def test_unusable_spec_added_in_place_is_skipped(screen: Screen):
    editor = _open_editor(screen)
    # An in-place change bypasses the setter's ValueError, so the spec is refused on the way out:
    # skipped with a warning, while the usable widget behind it still renders.
    unusable = {'kind': 'widget', 'position': 5, 'text': 42, 'class': 'cm-test-no-text'}
    editor.decorations.append(unusable)  # type: ignore[arg-type]
    editor.decorations.append({'kind': 'widget', 'position': 5, 'text': 'hint', 'class': 'cm-test-late-hint'})
    screen.wait_for(lambda: _span_count(screen, 'cm-test-late-hint') == 1)
    assert _span_count(screen, 'cm-test-no-text') == 0, \
        'a widget without usable text is skipped instead of rendering an empty span'
    screen.assert_py_logger('WARNING', re.compile(r"needs a string 'text'"))


def test_empty_replace_range_is_skipped(screen: Screen):
    editor = _open_editor(screen)
    editor.decorations = [
        {'kind': 'replace', 'from': 6, 'to': 6, 'text': 'nothing', 'class': 'cm-test-empty'},
        # An empty range is legal for CodeMirror as long as it is inclusive, so this one survives.
        {'kind': 'replace', 'from': 8, 'to': 8, 'text': 'INS', 'class': 'cm-test-empty-incl', 'inclusive': True},
    ]
    screen.wait_for(lambda: _span_count(screen, 'cm-test-empty-incl') == 1)
    assert _span_count(screen, 'cm-test-empty') == 0
    screen.assert_py_logger('WARNING', re.compile(r'replace range is empty'))


def test_decoration_inclusive_end_extends_mark(screen: Screen):
    editor = _open_editor(screen)
    editor.decorations = [{'kind': 'mark', 'from': 6, 'to': 10, 'inclusiveEnd': True, 'class': 'cm-test-incl'}]
    screen.wait_for(lambda: _span_count(screen, 'cm-test-incl') == 1)
    # Insert exactly at the mark's right edge (offset 10). Only a live inclusiveEnd grows the mark
    # over the new character; a plain mapped mark (default exclusive end) would still read "beta".
    editor.value = editor.value[:10] + 'Z' + editor.value[10:]
    screen.wait_for_js('document.querySelector(".cm-content").innerText.includes("betaZ")', True)
    grown = _marked_text(screen, 'cm-test-incl')
    assert grown == 'betaZ'


def test_line_tooltip_api(screen: Screen):
    @ui.page('/')
    def page():
        editor = ui.codemirror('alpha\nbeta\ngamma').classes('w-24')
        ui.button('Set tooltip on line 2', on_click=lambda: editor.line_tooltips.__setitem__(2, 'debug'))
        ui.button('Set tooltip on line 3', on_click=lambda: editor.line_tooltips.__setitem__(3, 'info'))
        ui.button('Delete tooltip on line 3', on_click=lambda: editor.line_tooltips.__delitem__(3))
        ui.button('Update tooltips', on_click=lambda: editor.line_tooltips.update({2: 'warning'}))
        ui.button('Replace tooltips', on_click=lambda: setattr(editor, 'line_tooltips', {1: 'error'}))
        ui.button('Clear tooltips', on_click=lambda: editor.line_tooltips.clear())  # pylint: disable=unnecessary-lambda

    screen.open('/')
    screen.click('Set tooltip on line 2')
    ActionChains(screen.selenium).move_to_element(screen.find('beta')).perform()
    screen.should_contain('debug')

    screen.click('Set tooltip on line 3')
    ActionChains(screen.selenium).move_to_element(screen.find('gamma')).perform()
    screen.should_contain('info')

    screen.click('Delete tooltip on line 3')
    ActionChains(screen.selenium).move_to_element(screen.find('gamma')).perform()
    screen.wait(0.5)
    screen.should_not_contain('info')

    screen.click('Update tooltips')
    ActionChains(screen.selenium).move_to_element(screen.find('beta')).perform()
    screen.should_contain('warning')

    screen.click('Replace tooltips')
    ActionChains(screen.selenium).move_to_element(screen.find('alpha')).perform()
    screen.should_contain('error')
    ActionChains(screen.selenium).move_to_element(screen.find('beta')).perform()
    screen.wait(0.5)
    screen.should_not_contain('warning')

    screen.click('Clear tooltips')
    ActionChains(screen.selenium).move_to_element(screen.find('alpha')).perform()
    screen.wait(0.5)
    screen.should_not_contain('error')


def test_line_tooltip_stick_to_text(screen: Screen):
    @ui.page('/')
    def page():
        editor = ui.codemirror('abc').classes('w-24')
        editor.line_tooltips[1] = 'tooltip'

    screen.open('/')
    ActionChains(screen.selenium).move_to_element(screen.find('abc')).click().send_keys(Keys.HOME, Keys.ENTER).perform()
    ActionChains(screen.selenium).move_to_element(screen.find('abc')).perform()
    screen.should_contain('tooltip')


def test_line_tooltip_plain_text_default(screen: Screen):
    @ui.page('/')
    def page():
        editor = ui.codemirror('hello').classes('w-24')
        editor.line_tooltips[1] = 'a < b'

    screen.open('/')
    ActionChains(screen.selenium).move_to_element(screen.find('hello')).perform()
    screen.should_contain('a < b')  # The tooltip should render the text as-is, not interpret it as HTML.


def test_line_tooltip_html_sanitized(screen: Screen):
    @ui.page('/')
    def page():
        editor = ui.codemirror('hello', line_tooltip_html=True).classes('w-24')
        editor.line_tooltips[1] = '<b>bold</b><img src=x onerror="console.error(`X` + `SS`)">'

    screen.open('/')
    ActionChains(screen.selenium).move_to_element(screen.find('hello')).perform()
    screen.should_contain('bold')  # The tooltip should render the allowed HTML...
    assert 'XSS' not in screen.selenium.get_log('browser')  # ...but sanitize out any scripts.


def test_decorations_track_edits_and_survive_an_unrelated_update(screen: Screen):
    editor = _open_editor(screen)
    editor.decorations = [{'kind': 'mark', 'from': 6, 'to': 10, 'class': 'cm-test-keep'}]
    screen.wait_for(lambda: _marked_text(screen, 'cm-test-keep') == 'beta')
    # Insert two characters before the mark: it follows "beta" instead of staying at the stale offsets 6..10.
    editor.value = 'XX' + editor.value
    screen.wait_for_js('document.querySelector(".cm-content").innerText.startsWith("XXalpha")', True)
    assert _marked_text(screen, 'cm-test-keep') == 'beta'
    # An unrelated update re-sends the props, which must not re-apply the declared offsets.
    editor.theme = 'basicDark'
    screen.wait_for_js(f'getElement({editor.id}).$props.theme', 'basicDark')
    assert _marked_text(screen, 'cm-test-keep') == 'beta'


def test_decorations_keep_their_text_after_an_astral_insert(screen: Screen):
    """Once an emoji precedes the mark, its str index and UTF-16 offset differ; the mark must still stay put."""
    document = 'a🎉b beta'
    editor = _open_editor(screen, document)
    start = document.index('beta')
    editor.decorations = [{'kind': 'mark', 'from': start, 'to': start + 4, 'class': 'cm-test-astral'}]
    screen.wait_for(lambda: _marked_text(screen, 'cm-test-astral') == 'beta')
    screen.selenium.execute_script(f'getElement({editor.id}).editor.dispatch({{changes: {{from: 0, insert: "🎉"}}}})')
    screen.wait_for(lambda: editor.value.startswith('🎉a'))
    editor.theme = 'basicDark'
    screen.wait_for_js(f'getElement({editor.id}).$props.theme', 'basicDark')
    assert _marked_text(screen, 'cm-test-astral') == 'beta'


def test_a_deleted_decoration_stays_gone(screen: Screen):
    editor = _open_editor(screen)
    editor.decorations = [{'kind': 'mark', 'from': 6, 'to': 10, 'class': 'cm-test-gone'}]
    screen.wait_for(lambda: _marked_text(screen, 'cm-test-gone') == 'beta')
    screen.selenium.execute_script(f'getElement({editor.id}).editor.dispatch({{changes: {{from: 6, to: 11}}}})')
    screen.wait_for(lambda: editor.value == 'alpha\ngamma')
    assert _marked_text(screen, 'cm-test-gone') is None, 'the mark vanishes with its text'
    # An unrelated update must not bring it back onto whatever sits at 6..10 now.
    editor.theme = 'basicDark'
    screen.wait_for_js(f'getElement({editor.id}).$props.theme', 'basicDark')
    assert _marked_text(screen, 'cm-test-gone') is None


def test_a_fold_survives_joining_its_last_line(screen: Screen):
    editor = _open_editor(screen, 'alpha\nbeta\ngamma\ndelta')
    editor.decorations = [{'kind': 'replace', 'from': 6, 'to': 16,
                           'text': '...', 'class': 'cm-test-fold', 'block': True}]
    screen.wait_for(lambda: _span_count(screen, 'cm-test-fold') == 1)
    # Deleting the newline after "gamma" leaves the fold ending mid-line, which CodeMirror keeps rendering.
    screen.selenium.execute_script(f'getElement({editor.id}).editor.dispatch({{changes: {{from: 16, to: 17}}}})')
    screen.wait_for(lambda: editor.value == 'alpha\nbeta\ngammadelta')
    assert _span_count(screen, 'cm-test-fold') == 1
    editor.theme = 'basicDark'
    screen.wait_for_js(f'getElement({editor.id}).$props.theme', 'basicDark')
    assert _span_count(screen, 'cm-test-fold') == 1


def test_decorations_survive_a_client_side_remount(screen: Screen):
    """A remount without a server round-trip must restore the mapped positions, not the declared ones."""
    editor: ui.codemirror = None  # type: ignore[assignment]

    @ui.page('/')
    def page():
        nonlocal editor
        with ui.tabs() as tabs:
            ui.tab('One')
            ui.tab('Two')
        with ui.tab_panels(tabs, value='One', keep_alive=False):
            with ui.tab_panel('One'):
                editor = ui.codemirror('alpha\nbeta\ngamma',
                                       decorations=[{'kind': 'mark', 'from': 6, 'to': 10, 'class': 'cm-test-remount'}])
            with ui.tab_panel('Two'):
                ui.label('Second tab')

    screen.open('/')
    screen.wait_for(lambda: _marked_text(screen, 'cm-test-remount') == 'beta')
    screen.selenium.execute_script(f'getElement({editor.id}).editor.dispatch({{changes: {{from: 0, insert: "XX"}}}})')
    screen.wait_for(lambda: editor.value.startswith('XXalpha'))
    # Leaving the tab destroys the editor client-side; coming back builds a fresh one from the props.
    screen.click('Two')
    screen.should_contain('Second tab')
    screen.click('One')
    screen.wait_for(lambda: _marked_text(screen, 'cm-test-remount') is not None)
    assert _marked_text(screen, 'cm-test-remount') == 'beta'
    # The server still holds the declared offsets; an unrelated update must not re-apply them.
    editor.theme = 'basicDark'
    screen.wait_for_js(f'getElement({editor.id}).$props.theme', 'basicDark')
    assert _marked_text(screen, 'cm-test-remount') == 'beta'


def test_writing_decorations_reapplies_declared_offsets(screen: Screen):
    """Like reassigning line anchors, any write applies the declared offsets afresh, so they must come from the current value."""
    editor = _open_editor(screen)
    editor.decorations = [{'kind': 'mark', 'from': 6, 'to': 10, 'class': 'cm-test-first'}]
    screen.wait_for(lambda: _marked_text(screen, 'cm-test-first') == 'beta')
    editor.value = editor.value[:6] + 'XX' + editor.value[6:]
    screen.wait_for_js('document.querySelector(".cm-content").innerText.includes("XXbeta")', True)
    assert _marked_text(screen, 'cm-test-first') == 'beta'
    # Appending is a write like any other: the stale first spec snaps back onto whatever sits at 6..10 now.
    start = editor.value.index('gamma')
    editor.decorations.append({'kind': 'mark', 'from': start, 'to': start + 5, 'class': 'cm-test-second'})
    screen.wait_for(lambda: _marked_text(screen, 'cm-test-second') == 'gamma')
    assert _marked_text(screen, 'cm-test-first') == 'XXbe'


@pytest.mark.parametrize('target', ['beta', '🎉'])
def test_decoration_offsets_are_python_string_indices(screen: Screen, target: str):
    """An offset computed with str.index() addresses the same text in the editor, astral chars included."""
    document = 'a🎉b beta'
    editor = _open_editor(screen, document)
    start = document.index(target)
    editor.decorations = [{
        'kind': 'mark', 'from': start, 'to': start + len(target), 'class': 'cm-test-astral',
    }]
    screen.wait_for(lambda: _marked_text(screen, 'cm-test-astral') == target)


async def test_decoration_specs_are_validated_on_assignment(user: User):
    """A spec no document could make sense of is refused where it is written, like a line anchor below 1."""
    editor: ui.codemirror = None  # type: ignore[assignment]

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('alpha\nbeta\ngamma')

    await user.open('/')
    with pytest.raises(ValueError, match='unknown kind'):
        editor.decorations = [{'kind': 'sparkle', 'from': 0, 'to': 1}]  # type: ignore[list-item]
    with pytest.raises(ValueError, match='missing required key'):
        editor.decorations = [{'kind': 'mark', 'from': 0}]  # type: ignore[list-item,typeddict-item]
    with pytest.raises(ValueError, match='from=4 > to=1'):
        editor.decorations = [{'kind': 'mark', 'from': 4, 'to': 1}]
    with pytest.raises(ValueError, match='offsets start at 0'):
        editor.decorations = [{'kind': 'widget', 'position': -1, 'text': '!'}]
    with pytest.raises(ValueError, match='lines are 1-indexed'):
        editor.decorations = [{'kind': 'line', 'line': 0}]


async def test_rejected_decorations_leave_no_editor_behind(user: User):
    """The constructor must refuse before the element registers itself, not halfway through building it."""
    @ui.page('/')
    def page():
        ui.label('Some content')

    await user.open('/')
    with user:
        with pytest.raises(ValueError, match='unknown kind'):
            ui.codemirror('alpha', decorations=[{'kind': 'sparkle'}])  # type: ignore[list-item]
    await user.should_not_see(ui.codemirror)


def _open_editor(screen: Screen, doc: str = 'alpha\nbeta\ngamma', **kwargs: Any) -> ui.codemirror:
    editor: ui.codemirror = None  # type: ignore[assignment]

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror(doc, **kwargs)

    screen.open('/')
    screen.wait_for(lambda: bool(screen.selenium.find_elements(By.CSS_SELECTOR, '.cm-content')))
    return editor


def _line_decoration_count(screen: Screen, css_class: str) -> int:
    return screen.selenium.execute_script(
        f'return document.querySelectorAll(".cm-line.{css_class}").length;'
    )


def _visible_text_length(screen: Screen) -> int:
    return screen.selenium.execute_script(
        'return document.querySelector(".cm-content").innerText.length;'
    )


def _span_count(screen: Screen, css_class: str) -> int:
    return screen.selenium.execute_script(
        f'return document.querySelectorAll(".cm-content span.{css_class}").length;'
    )


def _marked_text(screen: Screen, css_class: str) -> str | None:
    return screen.selenium.execute_script(
        f'const s = document.querySelector(".cm-content span.{css_class}"); return s ? s.textContent : null;')
