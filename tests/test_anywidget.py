import anywidget
import pytest
import traitlets

from nicegui import ui
from nicegui.testing import Screen, User


async def test_delete_stops_observing_the_widget(user: User, caplog: pytest.LogCaptureFixture):
    """A widget can outlive its element (e.g. in a refreshable), so deleting the element has to unobserve it."""
    class SharedWidget(anywidget.AnyWidget):  # pylint: disable=abstract-method
        _esm = 'export default {};'
        value = traitlets.Int(0).tag(sync=True)

    widget = SharedWidget()
    element = None

    @ui.page('/')
    def page():
        nonlocal element
        element = ui.anywidget(widget)

    await user.open('/')
    assert not [record for record in caplog.records if 'still being used' in record.message]

    element.delete()
    widget.value = 1
    assert not [record for record in caplog.records if 'still being used' in record.message], \
        'changing a trait of a deleted element must not warn anymore'


def test_anywidget(screen: Screen):
    class CounterWidget(anywidget.AnyWidget):  # pylint: disable=abstract-method
        _esm = '''
            function render({ model, el }) {
                const button = document.createElement("button");
                button.innerHTML = `anywidget: ${model.get("value")}`;
                button.addEventListener("click", () => {
                    model.set("value", model.get("value") + 1);
                    model.save_changes();
                });
                model.on("change:value", () => (button.innerHTML = `anywidget: ${model.get("value")}`));
                el.appendChild(button);
            }
            export default { render };
        '''
        value = traitlets.Int(0).tag(sync=True)

    @ui.page('/')
    def page():
        counter = CounterWidget(value=42)
        ui.anywidget(counter)

        @ui.button().bind_text_from(counter, 'value', backward=lambda c: f'NiceGUI: {c}').on_click
        def increment_counter() -> None:
            counter.value += 1

    screen.open('/')
    screen.click('anywidget: 42')
    screen.click('NiceGUI: 43')
    screen.should_contain('anywidget: 44')


def test_nested_update(screen: Screen):
    class UpdateWidget(anywidget.AnyWidget):  # pylint: disable=abstract-method
        _esm = '''
            function render({model, el}) {
                const div = document.createElement("div");
                div.innerText = "nothing";
                el.appendChild(div);
                model.on("change:b", () => div.innerText = `b=${model.get("b")}`);
                model.set("a", 1);
                model.save_changes();
            }
            export default { render };
        '''
        a = traitlets.Int(0).tag(sync=True)
        b = traitlets.Int(0).tag(sync=True)

    @ui.page('/')
    def page():
        uw = UpdateWidget()

        def change_b(change):
            """Change the value of `b` while handling the change of `a`."""
            assert change['name'] == 'a'
            assert change['new'] == 1
            uw.b = 1
        uw.observe(change_b, names=['a'])
        ui.anywidget(uw)

    screen.open('/')
    screen.should_contain('b=1')


@pytest.mark.parametrize('initialize_return,expected_events', [
    ('() => record("cleanup:initialize")',
     ['abort:initialize', 'cleanup:initialize', 'abort:render', 'cleanup:render']),
    ('{ some_export: () => record("export") }',
     ['abort:initialize', 'abort:render', 'cleanup:render']),
])
def test_lifecycle_cleanup_on_delete(screen: Screen, initialize_return: str, expected_events: list[str]):
    """Deleting the element aborts the AFM signal and runs the cleanups returned by `initialize` and `render`.

    `initialize` may also return an object of exports, which must not be called as a cleanup.
    """
    class CleanupWidget(anywidget.AnyWidget):  # pylint: disable=abstract-method
        _esm = '''
            const record = (event) => (window.events ??= []).push(event);
            function initialize({ model, signal }) {
                signal.addEventListener("abort", () => record("abort:initialize"));
                return INITIALIZE_RETURN;
            }
            function render({ model, el, signal }) {
                el.innerText = "widget";
                record("render");
                signal.addEventListener("abort", () => record("abort:render"));
                return () => record("cleanup:render");
            }
            export default { initialize, render };
        '''.replace('INITIALIZE_RETURN', initialize_return)

    @ui.page('/')
    def page():
        element = ui.anywidget(CleanupWidget())
        ui.button('Delete', on_click=element.delete)

    screen.open('/')
    screen.wait_for_js('window.events.length', 1)  # render ran and recorded the mounted view
    screen.click('Delete')
    screen.wait_for_js('window.events.length', 1 + len(expected_events))
    assert screen.selenium.execute_script('return window.events') == ['render', *expected_events]


def test_off_removes_listener(screen: Screen):
    """`model.off` has to remove a single callback; AFM widgets use it to unsubscribe in their cleanup."""
    class OffWidget(anywidget.AnyWidget):  # pylint: disable=abstract-method
        _esm = '''
            export function render({ model, el }) {
                el.innerText = "listening";
                const callback = () => (el.innerText = "notified");
                model.on("change:value", callback);
                model.off("change:value", callback);
            }
        '''
        value = traitlets.Int(0).tag(sync=True)

    @ui.page('/')
    def page():
        widget = OffWidget()
        ui.anywidget(widget)
        ui.button('Change', on_click=lambda: setattr(widget, 'value', 1))

    screen.open('/')
    screen.should_contain('listening')  # render ran and subscribed/unsubscribed
    screen.click('Change')
    screen.should_not_contain('notified')
