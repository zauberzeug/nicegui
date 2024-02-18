from nicegui import ui

from . import doc


@doc.demo(ui.slider)
def main_demo() -> None:
    slider = ui.slider(min=0, max=100, value=50)
    ui.label().bind_text_from(slider, 'value')


@doc.demo('Throttle events with leading and trailing options', '''
    By default the value change event of a slider is throttled to 0.05 seconds.
    This means that if you move the slider quickly, the value will only be updated every 0.05 seconds.

    By default both "leading" and "trailing" events are activated.
    This means that the very first event is triggered immediately, and the last event is triggered after the throttle time.

    This demo shows how disabling either of these options changes the behavior.
    To see the effect more clearly, the throttle time is set to 1 second.
    The first slider shows the default behavior, the second one only sends leading events, and the third only sends trailing events.
''')
def throttle_events_with_leading_and_trailing_options():
    ui.label('default')
    ui.slider(min=0, max=10, step=0.1, value=5).props('label-always') \
        .on('update:model-value', lambda e: ui.notify(e.args),
            throttle=1.0)

    ui.label('leading events only')
    ui.slider(min=0, max=10, step=0.1, value=5).props('label-always') \
        .on('update:model-value', lambda e: ui.notify(e.args),
            throttle=1.0, trailing_events=False)

    ui.label('trailing events only')
    ui.slider(min=0, max=10, step=0.1, value=5).props('label-always') \
        .on('update:model-value', lambda e: ui.notify(e.args),
            throttle=1.0, leading_events=False)


@doc.demo('Disable slider', '''
    You can disable a slider with the `disable()` method.
    This will prevent the user from moving the slider.
    The slider will also be grayed out.
''')
def disable_slider():
    slider = ui.slider(min=0, max=100, value=50)
    ui.button('Disable slider', on_click=slider.disable)
    ui.button('Enable slider', on_click=slider.enable)


doc.reference(ui.slider)
