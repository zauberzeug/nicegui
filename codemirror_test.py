from nicegui import ui

cm = ui.codemirror("Test123", on_change=lambda event: print(event.value))

cm.on_value_change(lambda: ui.notify(cm.value))
ui.input("Type here").bind_value(cm)

ui.run(dark=True)
