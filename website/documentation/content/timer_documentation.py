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


@doc.demo('Reset or Trigger timer on interval change', '''
    It may be desirable to immediately honor the new interval when it is set.

    For example, if a timer was set with long interval (600 seconds), and it was updated to shorter interval (10 seconds), the intention may not be to wait for the remaining time, which may be well in excess of the new interval.

    ui.timer supports on_interval_changed to run a callback of your desire, which can be:

    - `.reset`: Simply reset the remaining time to the updated interval, but will not immediately run the timer callback.
    - `.trigger`: The above, but also runs the timer callback (imagine turning a clock forward until the alarm rings)
    - A custom callback which you can run the above methods, based on whether the interval was increased or decreased.

    We believe that the default behavior, reset-on-change, trigger-on-change all have their own use cases, and we offer the maximum flexibility to the developer.

    In the following example, observe:

    - Timer 1 is not affected by the interval change. It does its own thing, waiting for the old interval to elapse before running the callback.
    - Timer 2 triggers the callback shortly after timer 3, by the new interval
    - Timer 3 triggers the callback immediately when the interval is changed
''')
def reset_or_trigger_demo():
    import time

    timer1_time = ui.label()
    timer1 = ui.timer(10, lambda: (timer1_time.set_text(
        f'Timer 1 triggered at {time.strftime("%X")}'), ui.notify('Timer 1 triggered')))

    timer2_time = ui.label()
    timer2 = ui.timer(10, lambda: (timer2_time.set_text(
        f'Timer 2 triggered at {time.strftime("%X")}'), ui.notify('Timer 2 triggered')))
    timer2.on_interval_changed(timer2.reset)

    timer3_time = ui.label()
    timer3 = ui.timer(10, lambda: (timer3_time.set_text(
        f'Timer 3 triggered at {time.strftime("%X")}'), ui.notify('Timer 3 triggered')))
    timer3.on_interval_changed(timer3.trigger)

    def set_all_timers(interval):
        for timer in (timer1, timer2, timer3):
            timer.interval = interval

    ui.button('Set all timers to 10 seconds', on_click=lambda: set_all_timers(10))
    ui.button('Set all timers to 30 seconds', on_click=lambda: set_all_timers(30))


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
