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


def test_lifecycle(screen: Screen):
    """The element drives the AFM lifecycle of its widget and tears it down when it is deleted.

    Both hooks get a `signal` which aborts on delete, the cleanup returned by `render` runs then,
    an object returned by `initialize` is kept as exports rather than called as a cleanup,
    `model.off` removes a single callback, and a deleted element stops observing its widget.
    """
    class LifecycleWidget(anywidget.AnyWidget):  # pylint: disable=abstract-method
        _esm = '''
            const record = (event) => (window.events ??= []).push(event);
            function initialize({ model, signal }) {
                signal.addEventListener("abort", () => record("abort:initialize"));
                return { some_export: () => record("export") };
            }
            function render({ model, el, signal }) {
                el.innerText = "widget";
                const callback = () => record("notified");
                model.on("change:value", callback);
                model.off("change:value", callback);
                model.on("change:value", () => record("changed"));
                signal.addEventListener("abort", () => record("abort:render"));
                record("render");
                return () => record("cleanup:render");
            }
            export default { initialize, render };
        '''
        value = traitlets.Int(0).tag(sync=True)

    widget = LifecycleWidget()

    @ui.page('/')
    def page():
        element = ui.anywidget(widget)
        ui.button('Change', on_click=lambda: setattr(widget, 'value', 1))
        ui.button('Delete', on_click=element.delete)

    screen.open('/')
    screen.wait_for_js('window.events', ['render'])
    screen.click('Change')
    screen.wait_for_js('window.events', ['render', 'changed'])  # the removed callback did not record "notified"
    screen.click('Delete')
    screen.wait_for_js('window.events', ['render', 'changed', 'abort:initialize', 'abort:render', 'cleanup:render'])
    widget.value = 2  # the widget outlives its element, e.g. in a refreshable
    assert not [record for record in screen.caplog.records if 'still being used' in record.message], \
        'a deleted element must not be updated anymore'
