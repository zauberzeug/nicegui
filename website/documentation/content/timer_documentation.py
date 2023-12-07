from nicegui import ui

from . import doc


@doc.demo(ui.timer)
def main_demo() -> None:
    from datetime import datetime

    label = ui.label()
    ui.timer(1.0, lambda: label.set_text(f'{datetime.now():%X}'))


@doc.demo('Activate, deactivate and cancel a timer', '''
    You can activate and deactivate a timer using the `active` property.
    You can cancel a timer using the `cancel` method.
    After canceling a timer, it cannot be activated anymore.
''')
def activate_deactivate_demo():
    slider = ui.slider(min=0, max=1, value=0.5)
    timer = ui.timer(0.1, lambda: slider.set_value((slider.value + 0.01) % 1.0))
    ui.switch('active').bind_value_to(timer, 'active')
    ui.button('Cancel', on_click=timer.cancel)


@doc.demo('Call a function after a delay', '''
    You can call a function after a delay using a timer with the `once` parameter.
''')
def call_after_delay_demo():
    def handle_click():
        ui.timer(1.0, lambda: ui.notify('Hi!'), once=True)
    ui.button('Notify after 1 second', on_click=handle_click)


doc.reference(ui.timer)
