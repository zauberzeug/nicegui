#!/usr/bin/env python3
from nice_gui import ui
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np
import time

with ui.card():
    ui.label('Interactive elements', 'h5')
    with ui.row():
        with ui.column():
            ui.button('Click me!', icon='touch_app', on_click=lambda: output.set_text('Click'))
            ui.checkbox('Check me!', on_change=lambda e: output.set_text('Checked' if e.value else 'Unchecked'))
            ui.switch('Switch me!', on_change=lambda e: output.set_text('Switched' if e.value else 'Unswitched'))
            ui.slider(0, 100, on_change=lambda e: output.set_text(e.value))
            ui.input('Text input', on_change=lambda e: output.set_text(e.value))
            ui.input('Number input', on_change=lambda e: output.set_text(e.value), type='number')
        with ui.column():
            ui.radio(['A', 'B', 'C'], on_change=lambda e: output.set_text(e.value))
            ui.select(['1', '2', '3'], on_change=lambda e: output.set_text(e.value))
    with ui.row():
        ui.label('Output:')
        output = ui.label()

with ui.card():
    ui.label('Timer', 'h5')
    with ui.row():
        ui.icon('far fa-clock')
        clock = ui.label()
        ui.timer(0.1, lambda: clock.set_text(datetime.now().strftime("%X")))

with ui.card():
    ui.label('Matplotlib', 'h5')
    with ui.plot(close=False) as plot:
        plt.title('Some plot')
        i, x, y = 0, [], []
        line, = plt.plot(x, y, 'C0')
        plt.ion()

    def update_plot():
        global i, x, y, line
        with plot:
            i += 1
            x = [*x, i][-100:]
            y = [*y, np.sin(time.time()) + 0.02 * np.random.randn()][-100:]
            line.set_xdata(x)
            line.set_ydata(y)
            plt.xlim(min(x), max(x))
            plt.ylim(min(y), max(y))

    ui.timer(0.1, update_plot)

ui.run()
