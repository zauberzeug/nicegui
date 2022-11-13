#!/usr/bin/env python3
from nicegui import ui

with ui.card():
    ui.label('Hello, world!')

with ui.card():
    ui.label('Events')
    ui.button('Click', on_click=lambda e: print(e, flush=True))
    ui.button('Notify', on_click=lambda _: ui.notify('Hello', closeBtn=True, type='info', color='red'))

with ui.card():
    ui.label('Binding')

    class Model:
        value = 'foo'

        def set_value(self, value: str):
            self.value = value
    model = Model()

    label1 = ui.label('Label 1')
    label2 = ui.label('Label 2').bind_text_from(label1)
    label3 = ui.label('Label 3').bind_text_from(model, 'value')

    ui.button('Change label 1', on_click=lambda: label1.set_text(label1.text + '!'))
    ui.button('Change label 2', on_click=lambda: label2.set_text(label2.text + '!'))
    ui.button('Change label 3', on_click=lambda: label3.set_text(label3.text + '!'))
    ui.button('Change model', on_click=lambda: model.set_value(model.value + '!'))

with ui.card():
    ui.label('Element gallery')
    ui.separator().classes('w-full')
    ui.icon('face')
    with ui.button('Click me!', on_click=lambda _: badge.set_text(int(badge.text) + 1)):
        badge = ui.badge('0', color='red').props('floating')
    ui.image('http://placeimg.com/640/360/tech').classes('w-full')
    c1 = ui.checkbox('Check A')
    c2 = ui.checkbox('Check B').bind_value_from(c1, 'value')
    ui.label('Visibility...').bind_visibility_from(c1, 'value')
    ui.button('Default', on_click=lambda: ui.colors())
    ui.button('Gray', on_click=lambda: ui.colors(primary='#555'))
    with ui.label('Tooltips...'):
        ui.tooltip('...are shown on mouse over').props('class=bg-orange')
    ui.html('<strong>HTML</strong>')

    ui.joystick(color='blue', size=50,
                on_start=lambda msg: print(msg, flush=True),
                on_move=lambda msg: coordinates.set_text(f"{msg['args']['data']['vector']['x']:.3f}, " +
                                                         f"{msg['args']['data']['vector']['y']:.3f}"),
                on_end=lambda msg: coordinates.set_text('0, 0')).style('width: 15em')
    coordinates = ui.label('0, 0')
    ui.link('Google', 'https://www.google.com/')
    ui.link('Target', '#target')
    ui.link_target('target')
    ui.markdown('**Markdown**')


ui.run(port=1234)
