from nicegui import ui


def main_demo() -> None:
    from datetime import datetime

    with ui.row().classes('items-center'):
        clock = ui.label()
        t = ui.timer(interval=0.1, callback=lambda: clock.set_text(datetime.now().strftime('%X.%f')[:-5]))
        ui.checkbox('active').bind_value(t, 'active')

    with ui.row():
        def lazy_update() -> None:
            new_text = datetime.now().strftime('%X.%f')[:-5]
            if lazy_clock.text[:8] == new_text[:8]:
                return
            lazy_clock.text = new_text
        lazy_clock = ui.label()
        ui.timer(interval=0.1, callback=lazy_update)
