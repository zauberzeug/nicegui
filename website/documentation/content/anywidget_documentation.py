from nicegui import ui

from . import doc

@doc.demo(ui.anywidget)
def main_demo() -> None:
    import anywidget
    import traitlets

    class CounterWidget(anywidget.AnyWidget):
        """Baseline anywidget example

        This is the getting started example from the anywidget documentation:
        https://anywidget.dev/en/getting-started/
        """
        _esm = '''
        function render({ model, el }) {
          let button = document.createElement("button");
          button.innerHTML = `anywidget count is ${model.get("value")}`;
          button.addEventListener("click", () => {
            model.set("value", model.get("value") + 1);
            model.save_changes();
          });
          model.on("change:value", () => {
            button.innerHTML = `anywidget count is ${model.get("value")}`;
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

    counter = CounterWidget(value=42)
    ui.anywidget(counter)

    def increment_counter():
        counter.value += 1
    ui.button(
        f'NiceGUI count is {counter.value}', on_click=increment_counter
    ).bind_text_from(counter, 'value', backward=lambda c: f'NiceGUI count is {c}')

    ui.run()

doc.reference(ui.anywidget)
