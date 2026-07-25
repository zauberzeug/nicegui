import pytest

from nicegui import ui
from nicegui.testing import Screen


@pytest.mark.parametrize('add_scroll_padding', [True, False])
def test_no_scroll_padding(screen: Screen, add_scroll_padding: bool):
    @ui.page('/')
    def page():
        ui.header(add_scroll_padding=add_scroll_padding).classes('h-[50px]')
        for i in range(100):
            with ui.link_target(f'line{i}'):
                ui.link(f'Line {i}', f'#line{i}')

    screen.open('/')
    screen.should_contain('Line 0')

    screen.click('Line 10')
    screen.wait(0.5)
    line_y = screen.selenium.execute_script("return arguments[0].getBoundingClientRect()['y'];", screen.find('Line 10'))
    if add_scroll_padding:
        assert line_y > 50
    else:
        assert line_y < 50


def test_scroll_padding_observer_disconnected(screen: Screen):
    @ui.page('/')
    def page():
        ui.add_head_html('''
            <script>
            window.__ro = [];
            const Orig = window.ResizeObserver;
            window.ResizeObserver = class extends Orig {
                constructor(cb) { super(cb); this.__rec = {targets: [], disconnected: false}; window.__ro.push(this.__rec); }
                observe(el, o) { this.__rec.targets.push((el && el.className) || ''); return super.observe(el, o); }
                disconnect() { this.__rec.disconnected = true; return super.disconnect(); }
            };
            </script>
        ''')
        header = ui.header()
        with header:
            ui.label('hi')
        ui.button('kill', on_click=header.delete)

    screen.open('/')
    screen.click('kill')
    screen.wait(0.5)
    records = screen.selenium.execute_script(
        "return window.__ro.filter(r => r.targets.some(t => t.includes('nicegui-header')));")
    assert records, 'expected at least one header-observing ResizeObserver'
    assert all(r['disconnected'] for r in records), f'leaked observers: {records}'
