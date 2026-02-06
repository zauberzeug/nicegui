import anywidget
import traitlets

from nicegui import ui
from nicegui.testing import SharedScreen


def test_anywidget(shared_screen: SharedScreen):
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

    shared_screen.open('/')
    shared_screen.click('anywidget: 42')
    shared_screen.click('NiceGUI: 43')
    shared_screen.should_contain('anywidget: 44')


def test_nested_update(shared_screen: SharedScreen):
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

    shared_screen.open('/')
    shared_screen.should_contain('b=1')
