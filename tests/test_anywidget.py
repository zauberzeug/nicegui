import anywidget
import traitlets

from nicegui import ui
from nicegui.testing import Screen


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


def test_lifecycle_cleanup_on_delete(screen: Screen):
    """Deleting the element aborts the AFM signal and runs the cleanups returned by `initialize` and `render`."""
    class CleanupWidget(anywidget.AnyWidget):  # pylint: disable=abstract-method
        _esm = '''
            const record = (event) => (window.events ??= []).push(event);
            function initialize({ model, signal }) {
                signal.addEventListener("abort", () => record("abort:initialize"));
                return () => record("cleanup:initialize");
            }
            function render({ model, el, signal }) {
                el.innerText = "widget";
                record("render");
                signal.addEventListener("abort", () => record("abort:render"));
                return () => record("cleanup:render");
            }
            export default { initialize, render };
        '''

    @ui.page('/')
    def page():
        element = ui.anywidget(CleanupWidget())
        ui.button('Delete', on_click=element.delete)

    screen.open('/')
    screen.wait_for_js('window.events.length', 1)  # render ran and recorded the mounted view
    screen.click('Delete')
    screen.wait_for_js('window.events.length', 5)
    events = screen.selenium.execute_script('return window.events')
    assert events[0] == 'render'
    assert sorted(events[1:]) == ['abort:initialize', 'abort:render', 'cleanup:initialize', 'cleanup:render']


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
    screen.click('Change')
    screen.should_contain('listening')
    screen.should_not_contain('notified')


def test_initialize_returning_exports(screen: Screen):
    """`initialize` may also return an object of exports, which must not be called as a cleanup on delete."""
    class ExportsWidget(anywidget.AnyWidget):  # pylint: disable=abstract-method
        _esm = '''
            function initialize() {
                return { some_export: () => "not a cleanup" };
            }
            function render({ model, el }) {
                el.innerText = "widget";
            }
            export default { initialize, render };
        '''

    @ui.page('/')
    def page():
        element = ui.anywidget(ExportsWidget())
        ui.button('Delete', on_click=element.delete)

    screen.open('/')
    screen.wait_for_js("document.body.innerText.includes('widget')", True)
    screen.click('Delete')
    screen.wait_for_js("document.body.innerText.includes('widget')", False)
