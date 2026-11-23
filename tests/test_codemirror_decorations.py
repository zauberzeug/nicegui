import re
from typing import Any

import pytest
from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import Screen, User


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
    editor = _open_editor(screen, decoration_html=True)
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
        {'kind': 'widget', 'position': 9999, 'text': '!', 'class': 'cm-test-past-end'},
        {'kind': 'line', 'line': 2, 'class': 'valid'},
    ]
    screen.wait_for(lambda: _line_decoration_count(screen, 'valid') == 1)
    assert _line_decoration_count(screen, 'out-of-range') == 0
    assert _span_count(screen, 'cm-test-past-end') == 0, 'an offset past the end is skipped, not clamped to it'
    screen.assert_py_logger('WARNING', re.compile(r'line 9999 out of range'))
    screen.assert_py_logger('WARNING', re.compile(r'position 9999 is past the end of the document'))


def test_unusable_spec_added_in_place_is_skipped(screen: Screen):
    editor = _open_editor(screen)
    # An in-place change bypasses the setter's ValueError, so the spec is refused on the way out:
    # skipped with a warning, while the usable widget behind it still renders.
    unusable = {'kind': 'widget', 'position': 5, 'text': 42, 'class': 'cm-test-no-text'}
    editor.decorations.append(unusable)
    editor.decorations.append({'kind': 'widget', 'position': 5, 'text': 'hint', 'class': 'cm-test-late-hint'})
    screen.wait_for(lambda: _span_count(screen, 'cm-test-late-hint') == 1)
    assert _span_count(screen, 'cm-test-no-text') == 0, \
        'a widget without usable text is skipped instead of rendering an empty span'
    screen.assert_py_logger('WARNING', re.compile(r"needs a string 'text'"))


def test_a_re_render_after_an_unusable_in_place_spec_still_mounts(screen: Screen):
    """A re-render builds the editor from the props verbatim, so the spec skipped on the way out must stay skipped."""
    editor = _open_editor(screen, decorations=[{'kind': 'mark', 'from': 6, 'to': 10, 'class': 'cm-test-kept'}])
    screen.wait_for(lambda: _marked_text(screen, 'cm-test-kept') == 'beta')
    editor.decorations.append({'kind': 'line', 'class': 'cm-test-broken'})
    editor.decorations.append({'kind': 'widget', 'position': 5, 'text': '!', 'class': 'cm-test-late'})
    screen.wait_for(lambda: _span_count(screen, 'cm-test-late') == 1)
    # A listener registered after the first render makes nicegui.js rebuild the element from the props.
    editor.on('focus', lambda: None)
    editor.theme = 'basicDark'
    screen.wait_for_js(f'getElement({editor.id}).$props.theme', 'basicDark')
    screen.wait_for(lambda: _marked_text(screen, 'cm-test-kept') == 'beta')
    assert _span_count(screen, 'cm-test-late') == 1


def test_a_kept_reference_to_the_list_stays_live_after_reassignment(screen: Screen):
    editor = _open_editor(screen)
    specs = editor.decorations
    editor.decorations = [{'kind': 'mark', 'from': 0, 'to': 5, 'class': 'cm-test-assigned'}]
    screen.wait_for(lambda: _marked_text(screen, 'cm-test-assigned') == 'alpha')
    specs.append({'kind': 'mark', 'from': 6, 'to': 10, 'class': 'cm-test-appended'})
    screen.wait_for(lambda: _marked_text(screen, 'cm-test-appended') == 'beta')


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


def test_decorations_declared_for_a_value_sent_in_the_same_update(screen: Screen):
    editor = _open_editor(screen)
    editor.value = 'XXXX' + editor.value
    start = editor.value.index('gamma')
    editor.decorations = [{'kind': 'mark', 'from': start, 'to': start + 5, 'class': 'cm-test-batch'}]
    screen.wait_for(lambda: _marked_text(screen, 'cm-test-batch') is not None)
    assert _marked_text(screen, 'cm-test-batch') == 'gamma'


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
    # An emoji makes the mapped UTF-16 offsets differ from the str indices the rebuilt props must carry.
    screen.selenium.execute_script(f'getElement({editor.id}).editor.dispatch({{changes: {{from: 0, insert: "🎉"}}}})')
    screen.wait_for(lambda: editor.value.startswith('🎉alpha'))
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
        editor.decorations = [{'kind': 'sparkle', 'from': 0, 'to': 1}]
    with pytest.raises(ValueError, match='missing required key'):
        editor.decorations = [{'kind': 'mark', 'from': 0}]
    with pytest.raises(ValueError, match='from=4 > to=1'):
        editor.decorations = [{'kind': 'mark', 'from': 4, 'to': 1}]
    with pytest.raises(ValueError, match='from=to=3'):
        editor.decorations = [{'kind': 'mark', 'from': 3, 'to': 3}]
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
            ui.codemirror('alpha', decorations=[{'kind': 'sparkle'}])
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
    return screen.selenium.execute_script(f'return document.querySelectorAll(".cm-line.{css_class}").length;')


def _visible_text_length(screen: Screen) -> int:
    return screen.selenium.execute_script('return document.querySelector(".cm-content").innerText.length;')


def _span_count(screen: Screen, css_class: str) -> int:
    return screen.selenium.execute_script(f'return document.querySelectorAll(".cm-content span.{css_class}").length;')


def _marked_text(screen: Screen, css_class: str) -> str | None:
    return screen.selenium.execute_script(
        f'const s = document.querySelector(".cm-content span.{css_class}"); return s ? s.textContent : null;')
