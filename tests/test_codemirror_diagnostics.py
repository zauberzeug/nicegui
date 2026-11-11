from nicegui import ui
from nicegui.testing import Screen


def _diagnostic_count(screen: Screen, suffix: str = '') -> int:
    selector = f'.cm-lintRange{suffix}'
    return screen.selenium.execute_script(f'return document.querySelectorAll({selector!r}).length;')


def _lint_panel_present(screen: Screen) -> bool:
    return screen.selenium.execute_script("return document.querySelector('.cm-panel-lint') !== null;")


def test_diagnostics_property(screen: Screen):
    editor = None
    counts: dict[str, dict[str, int]] = {}

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('Line 1\nLine 2\nLine 3')

        async def snapshot(key: str):
            counts[key] = await editor.get_diagnostic_count()
            ui.label(f'snapshot-{key}')

        ui.button('SnapAfterSet', on_click=lambda: snapshot('after_set'))
        ui.button('SnapAfterClear', on_click=lambda: snapshot('after_clear'))

    screen.open('/')
    editor.diagnostics = [
        {'line': 1, 'message': 'oops', 'severity': 'error'},
        {'line': 3, 'message': 'note', 'severity': 'info'},
        {'line': 2, 'message': 'col mark', 'severity': 'warning', 'column': 2, 'end_column': 5},
    ]
    screen.wait_for(lambda: _diagnostic_count(screen) == 3)
    assert _diagnostic_count(screen, '-error') >= 1
    assert _diagnostic_count(screen, '-info') >= 1
    assert _diagnostic_count(screen, '-warning') >= 1

    # Column-targeted diagnostic must produce a sub-line mark.
    widths = screen.selenium.execute_script(
        "return Array.from(document.querySelectorAll('.cm-lintRange-warning'))"
        '.map(m => m.getBoundingClientRect().width);'
    )
    line_width = screen.selenium.execute_script(
        "const lines = document.querySelectorAll('.cm-line');"
        'return lines[1].getBoundingClientRect().width;'
    )
    assert widths and all(0 < w < line_width for w in widths)

    screen.click('SnapAfterSet')
    screen.wait_for('snapshot-after_set')
    assert counts['after_set'] == {'error': 1, 'warning': 1, 'info': 1, 'hint': 0, 'total': 3}

    editor.diagnostics = []
    screen.wait_for(lambda: _diagnostic_count(screen) == 0)

    screen.click('SnapAfterClear')
    screen.wait_for('snapshot-after_clear')
    assert counts['after_clear'] == {'error': 0, 'warning': 0, 'info': 0, 'hint': 0, 'total': 0}

    editor.diagnostics = [{'line': 2, 'message': 'no severity'}]
    screen.wait_for(lambda: _diagnostic_count(screen, '-error') == 1)

    editor.open_lint_panel()
    screen.wait_for(lambda: _lint_panel_present(screen))
    editor.close_lint_panel()
    screen.wait_for(lambda: not _lint_panel_present(screen))
    editor.toggle_lint_panel()
    screen.wait_for(lambda: _lint_panel_present(screen))
    editor.toggle_lint_panel()
    screen.wait_for(lambda: not _lint_panel_present(screen))


def test_diagnostic_message_default_is_plain_text(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('alpha\nbeta\ngamma')

    screen.open('/')
    editor.diagnostics = [
        {'line': 2, 'message': '<b>raw</b>'},
    ]
    screen.wait_for(lambda: _diagnostic_count(screen) == 1)
    editor.open_lint_panel()
    screen.wait_for(lambda: _lint_panel_present(screen))
    has_bold = screen.selenium.execute_script(
        'const p = document.querySelector(".cm-panel-lint");'
        'return !!(p && p.querySelector("b"));'
    )
    text = screen.selenium.execute_script(
        'const p = document.querySelector(".cm-panel-lint");'
        'return p ? p.textContent : "";'
    )
    assert not has_bold, 'default rendering must not interpret HTML'
    assert '<b>raw</b>' in text, 'default rendering shows raw tags as visible text'


def test_diagnostic_message_html_opt_in_renders_sanitized(screen: Screen):
    editor = None

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror('alpha\nbeta\ngamma', diagnostic_message_html=True)

    screen.open('/')
    editor.diagnostics = [
        {'line': 2, 'message': '<b>safe</b><script>window.__diag_hijack=1</script>'},
    ]
    screen.wait_for(lambda: _diagnostic_count(screen) == 1)
    editor.open_lint_panel()
    screen.wait_for(lambda: _lint_panel_present(screen))
    screen.wait_for(lambda: screen.selenium.execute_script(
        'const p = document.querySelector(".cm-panel-lint");'
        'return !!(p && p.querySelector("b"));'
    ))
    has_script = screen.selenium.execute_script(
        'const p = document.querySelector(".cm-panel-lint");'
        'return !!(p && p.querySelector("script"));'
    )
    hijacked = screen.selenium.execute_script('return window.__diag_hijack === 1')
    assert not has_script, 'DOMPurify should have stripped <script>'
    assert not hijacked, 'inline script must not have executed'
