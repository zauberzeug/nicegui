#!/usr/bin/env python3
from nicegui import ui
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np

with ui.row():
    with ui.card():
        ui.label('Interactive elements', 'h5')
        with ui.row():
            with ui.column():
                ui.button('Click me!', icon='touch_app', design='outline rounded',
                          on_click=lambda: output.set_text('Click'))
                ui.checkbox('Check me!', on_change=lambda e: output.set_text('Checked' if e.value else 'Unchecked'))
                ui.switch('Switch me!', on_change=lambda e: output.set_text('Switched' if e.value else 'Unswitched'))
                ui.slider(0, 100, on_change=lambda e: output.set_text(e.value))
                ui.input(label='Text', on_change=lambda e: output.set_text(e.value))
                ui.number(label='Number', on_change=lambda e: output.set_text(e.value), value=3.1415927, decimals=2)
            with ui.column():
                ui.radio(options=['A', 'B', 'C'], value='A', on_change=lambda e: output.set_text(e.value))
                ui.select(options=['a', 'b', 'c'], value='a', on_change=lambda e: output.set_text(e.value))
            with ui.column():
                ui.radio(options={1: 'A', 2: 'B', 3: 'C'}, on_change=lambda e: output.set_text(e.value))
                ui.select(options={1: 'a', 2: 'b', 3: 'c'}, on_change=lambda e: output.set_text(e.value))
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
