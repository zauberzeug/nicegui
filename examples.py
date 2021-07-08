#!/usr/bin/env python3
from nicegui import ui
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np

with ui.row():
    with ui.card():
        ui.label('Interactive elements').classes('text-h5')
        with ui.row():
            with ui.column():
                ui.button('Click me!', on_click=lambda: output.set_text('Click'))
                ui.checkbox('Check me!', on_change=lambda e: output.set_text('Checked' if e.value else 'Unchecked'))
                ui.switch('Switch me!', on_change=lambda e: output.set_text('Switched' if e.value else 'Unswitched'))
                ui.slider(min=0, max=100, value=50, step=0.1, on_change=lambda e: output.set_text(e.value))
                ui.input(label='Text', value='abc', on_change=lambda e: output.set_text(e.value))
                ui.number(label='Number', value=3.1415927, format='%.2f', on_change=lambda e: output.set_text(e.value))
            with ui.column():
                with ui.row():
                    ui.radio(options=['A', 'B', 'C'], value='A', on_change=lambda e: output.set_text(e.value))
                    ui.radio(options={1: 'o', 2: 'oo', 3: 'ooo'}, value=1, on_change=lambda e: output.set_text(e.value))
                with ui.row():
                    ui.select(options=['a', 'b', 'c'], value='a', on_change=lambda e: output.set_text(e.value))
                    ui.select(options={1: 'a', 2: 'b', 3: 'c'}, value=1, on_change=lambda e: output.set_text(e.value))
                ui.toggle(['1', '2', '3'], value='1', on_change=lambda e: output.set_text(e.value))
                ui.toggle({1: 'X', 2: 'Y', 3: 'Z'}, value=1, on_change=lambda e: output.set_text(e.value))
        ui.radio(['x', 'y', 'z'], value='x', on_change=lambda e: output.set_text(e.value)).props('inline color=green')
        with ui.row():
            ui.label('Output:')
            output = ui.label('').classes('text-bold')

    with ui.column():
        with ui.card():
            ui.label('Timer').classes('text-h5')
            with ui.row():
                ui.icon('far fa-clock')
                clock = ui.label()
                t = ui.timer(0.1, lambda: clock.set_text(datetime.now().strftime("%X")))
            ui.checkbox('active').bind_value(t.active)

        with ui.card().classes('items-center'):
            ui.label('Style').classes('text-h5')
            ui.icon('fas fa-umbrella-beach').props('size=70px').classes('text-amber-14').style('margin: 9px')
            ui.link('color palette', 'https://quasar.dev/style/color-palette')
            ui.button().props('icon=touch_app outline round')

    with ui.card():
        ui.label('Binding').classes('text-h5')
        with ui.row():
            n1 = ui.number(value=1.2345, format='%.2f')
            n2 = ui.number(format='%.3f').bind_value(n1.value)
        with ui.row():
            c = ui.checkbox('c1')
            ui.switch('c2').bind_value(c.value)
            ui.slider(min=0, max=1, value=0.5, step=0.01).bind_value_to(c.value, forward=lambda f: f > 0.5)
        with ui.row():
            model = type('Model', (), {'value': 1})  # one-liner to define an object with an attribute "value"
            ui.radio({1: 'a', 2: 'b', 3: 'c'}).bind_value(model.value)
            ui.radio({1: 'A', 2: 'B', 3: 'C'}).bind_value(model.value)
            with ui.column():
                ui.number().bind_value(model.value)
                ui.slider(min=1, max=3).bind_value(model.value)
                ui.label().bind_text(model.value)
        with ui.row().classes('items-center'):
            v = ui.checkbox('visible', value=True)
            ui.icon('visibility').bind_visibility_from(v.value)

    with ui.card():
        ui.label('Matplotlib').classes('text-h5')
        with ui.plot(close=False) as plot:
            plt.title('Some plot')
            x, y = [], []
            line, = plt.plot(x, y, 'C0')

        def update_plot():
            global x, y, line
            with plot:
                x = [*x, datetime.now()][-50:]
                y = [*y, np.sin(0.5 * datetime.now().timestamp()) + 0.02 * np.random.randn()][-50:]
                line.set_xdata(x)
                line.set_ydata(y)
                plt.xlim(min(x), max(x))
                plt.ylim(min(y), max(y))

        ui.timer(0.5, update_plot)

    with ui.card():
        ui.label('Line Plot').classes('text-h5')
        lines = ui.line_plot(n=2, limit=200, update_every=5).with_legend(['sin', 'cos'], loc='upper center', ncol=2)
        ui.timer(0.1, lambda: lines.push([datetime.now()], [
            [np.sin(datetime.now().timestamp()) + 0.02 * np.random.randn()],
            [np.cos(datetime.now().timestamp()) + 0.02 * np.random.randn()],
        ]))

ui.run()
