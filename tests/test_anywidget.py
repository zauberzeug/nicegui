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
