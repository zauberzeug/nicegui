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


@doc.demo('Cancel current invocation', '''
    If you also want to cancel the currently invoked task of the callback,
    just call the `cancel` method with the `with_current_invocation` parameter set to `True`.

    The following demo shows a timer that runs every 2.5 seconds and displays a progress bar that fills up over 2 seconds.
    If you cancel the timer by clicking the "Cancel" button, the current cycle continues until completion.
    The "Cancel with current invocation" button, however, will also cancel the currently running cycle.

    *Added in version 2.23.0*
''')
def cancel_timer_demo():
    import asyncio

    progress = ui.linear_progress().props('instant-feedback')

    async def cycle_once():
        for i in range(10):
            progress.value = (i + 1) / 10
            await asyncio.sleep(0.2)

    def start_progress():
        timer = ui.timer(2.5, cycle_once, immediate=True)
        with ui.column() as controls:
            ui.button('Cancel') \
                .on('click', lambda: timer.cancel(with_current_invocation=False)) \
                .on('click', controls.delete)
            ui.button('Cancel with current invocation') \
                .on('click', lambda: timer.cancel(with_current_invocation=True)) \
                .on('click', controls.delete)

    ui.button('Start progress', on_click=start_progress).props('flat')


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
