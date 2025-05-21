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


@doc.demo("Don't start immediately", '''
    By default, the timer will start immediately.
    You can change this behavior by setting the `immediate` parameter to `False`.
    This will delay the first execution of the callback by the given interval.

    *Added in version 2.9.0*
''')
def start_immediately_demo():
    from datetime import datetime

    label = ui.label()
    ui.timer(1.0, lambda: label.set_text(f'{datetime.now():%X}'), immediate=False)


@doc.demo('Global app timer', '''
    While `ui.timer` is kind of a UI element that runs in the context of the current page,
    you can also use the global `app.timer` for UI-independent timers.

    *Added in version 2.9.0*
''')
def app_timer_demo():
    from nicegui import app

    counter = {'value': 0}
    app.timer(1.0, lambda: counter.update(value=counter['value'] + 1))

    # @ui.page('/')
    def page():
        ui.label().bind_text_from(counter, 'value', lambda value: f'Count: {value}')
    page()  # HIDE


doc.reference(ui.timer)
