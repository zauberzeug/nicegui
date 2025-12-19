import anywidget
import traitlets

from nicegui import ui
from nicegui.testing import Screen


def test_anywidget(screen: Screen):
    class CounterWidget(anywidget.AnyWidget):  # pylint: disable=abstract-method
        """Baseline AnyWidget example from https://anywidget.dev/en/getting-started/."""
        _esm = '''
        function render({ model, el }) {
          let button = document.createElement("button");
          button.innerHTML = `AnyWidget count is ${model.get("value")}`;
          button.addEventListener("click", () => {
            model.set("value", model.get("value") + 1);
            model.save_changes();
          });
          model.on("change:value", () => {
            button.innerHTML = `AnyWidget count is ${model.get("value")}`;
          });
          el.classList.add("counter-widget");
          el.appendChild(button);
        }
        export default { render };
        '''
        _css = '''
        .counter-widget button { color: white; font-size: 1.75rem; background-color: #ea580c; padding: 0.5rem 1rem; border: none; border-radius: 0.25rem; }
        .counter-widget button:hover { background-color: #9a3412; }
        '''
        value = traitlets.Int(0).tag(sync=True)

    @ui.page('/')
    def page():
        counter = CounterWidget(value=42)
        ui.anywidget(counter)

        def increment_counter():
            counter.value += 1
        ui.button(f'NiceGUI count is {counter.value}', on_click=increment_counter) \
          .bind_text_from(counter, 'value', backward=lambda c: f'NiceGUI count is {c}')

    screen.open('/')
    screen.click('AnyWidget count is 42')
    screen.click('NiceGUI count is 43')
    screen.should_contain('AnyWidget count is 44')
