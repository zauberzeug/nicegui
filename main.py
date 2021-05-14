#!/usr/bin/env python3
from nicegui import ui
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np

with ui.card(), ui.row():
    ui.label('Binding', 'h5')
    n1 = ui.number(value=0.5, format='%.2f', on_change=lambda e: print(e.value))
    n2 = ui.number(format='%.3f').bind('value', n1, 'value')

    c1 = ui.checkbox('c1', value=True, on_change=lambda e: print(e.value))
    s1 = ui.switch('c2', value=True, on_change=lambda e: print(e.value))

    c2 = ui.checkbox('c2', on_change=lambda e: print(e.value))
    s2 = ui.switch('s2', on_change=lambda e: print(e.value)).bind('value', c2, 'value')

with ui.row():
    with ui.card():
        ui.label('Interactive elements', 'h5')
        with ui.row():
            with ui.column():
                ui.button('Click me!', icon='touch_app', design='outline rounded',
                          on_click=lambda: output.set_text('Click'))
                ui.checkbox('Check me!', on_change=lambda e: output.set_text('Checked' if e.value else 'Unchecked'))
                ui.switch('Switch me!', on_change=lambda e: output.set_text('Switched' if e.value else 'Unswitched'))
                ui.slider(min=0, max=100, value=50, step=0.1, on_change=lambda e: output.set_text(e.value))
                ui.input(label='Text', value='abc', on_change=lambda e: output.set_text(e.value))
                ui.number(label='Number', value=3.1415927, format='%.2f', on_change=lambda e: output.set_text(e.value))
            with ui.column():
                with ui.row():
                    ui.radio(options=['A', 'B', 'C'], value='A', on_change=lambda e: output.set_text(e.value))
                    ui.radio(options={1: 'A', 2: 'B', 3: 'C'}, value=1, on_change=lambda e: output.set_text(e.value))
                with ui.row():
                    ui.select(options=['a', 'b', 'c'], value='a', on_change=lambda e: output.set_text(e.value))
                    ui.select(options={1: 'a', 2: 'b', 3: 'c'}, value=1, on_change=lambda e: output.set_text(e.value))
                ui.toggle(['1', '2', '3'], value='1', on_change=lambda e: output.set_text(e.value))
                ui.toggle({1: 'X', 2: 'Y', 3: 'Z'}, value=1, on_change=lambda e: output.set_text(e.value))
        with ui.row():
            ui.label('Output:')
            output = ui.label()

    with ui.column():
        with ui.card():
            ui.label('Timer', 'h5')
            with ui.row():
                ui.icon('far fa-clock')
                clock = ui.label()
                ui.timer(0.1, lambda: clock.set_text(datetime.now().strftime("%X")))

        with ui.card():
            ui.label('Style', 'h5')
            ui.icon('fas fa-umbrella-beach', size='88px', color='amber-14')
            ui.link('color palette', 'https://quasar.dev/style/color-palette')

    with ui.card():
        ui.label('Matplotlib', 'h5')
        with ui.plot(close=False) as plot:
            plt.title('Some plot')
            x, y = [], []
            line, = plt.plot(x, y, 'C0')

        def update_plot():
            global x, y, line
            with plot:
                x = [*x, datetime.now()][-100:]
                y = [*y, np.sin(datetime.now().timestamp()) + 0.02 * np.random.randn()][-100:]
                line.set_xdata(x)
                line.set_ydata(y)
                plt.xlim(min(x), max(x))
                plt.ylim(min(y), max(y))

        ui.timer(1.0, update_plot)

    with ui.card():
        ui.label('Line Plot', 'h5')
        lines = ui.line_plot(n=2, limit=20).with_legend(['sin', 'cos'], loc='upper center', ncol=2)
        ui.timer(1.0, lambda: lines.push([datetime.now()], [
            [np.sin(datetime.now().timestamp()) + 0.02 * np.random.randn()],
            [np.cos(datetime.now().timestamp()) + 0.02 * np.random.randn()],
        ]))
