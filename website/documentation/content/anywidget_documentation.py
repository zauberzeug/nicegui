from nicegui import ui

from . import doc


@doc.demo(ui.anywidget)
def main_demo() -> None:
    import anywidget
    import traitlets

    class CounterWidget(anywidget.AnyWidget):
        _esm = '''
            function render({ model, el }) {
                const button = document.createElement("button");
                button.innerHTML = `Count is ${model.get("value")}`;
                button.addEventListener("click", () => {
                    model.set("value", model.get("value") + 1);
                    model.save_changes();
                });
                model.on("change:value", () => {
                    button.innerHTML = `Count is ${model.get("value")}`;
                });
                el.classList.add("counter-widget");
                el.appendChild(button);
            }
            export default { render };
        '''
        _css = '''
            .counter-widget button {
                color: white;
                background-color: DarkOrange;
                padding: 0.5rem 1rem;
                border-radius: 0.25rem;
                cursor: pointer;

                &:hover {
                    opacity: 0.8;
                }
            }
        '''
        value = traitlets.Int(0).tag(sync=True)

        def increment(self) -> None:
            self.value += 1

    counter = CounterWidget(value=42)
    ui.anywidget(counter)

    ui.label('↑ AnyWidget')
    ui.separator()
    ui.label('↓ NiceGUI')

    ui.button(on_click=counter.increment) \
      .bind_text_from(counter, 'value', backward=lambda c: f'Count is {c}')


doc.reference(ui.anywidget)
