#!/usr/bin/env python3
from nice_gui import ui
from datetime import datetime
from matplotlib import pyplot as plt

with ui.card():
    ui.label('Rows and columns', 'h5')
    with ui.row():
        ui.label('A')
        ui.label('B')
        with ui.column():
            ui.label('C1')
            ui.label('C2')
            ui.label('C3')

with ui.card():
    ui.label('Timer', 'h5')
    time = ui.label()
    ui.timer(0.1, lambda: time.set_text(datetime.now().strftime("%X")))

with ui.card():
    ui.label('Interactive elements', 'h5')
    ui.button('Click me!', on_click=lambda: output.set_text('Click'))
    ui.checkbox('Check me!', on_change=lambda e: output.set_text('Checked' if e.value else 'Unchecked'))
    ui.radio(['A', 'B', 'C'], on_change=lambda e: output.set_text(e.value))
    output = ui.label()

with ui.card():
    ui.label('Matplotlib', 'h5')
    with ui.plot(close=False) as plot:
        plt.title('Some plot')
        plt.plot(range(10), [x**2 for x in range(10)])

    def update_plot():
        plt.title('Some plot with a second curve')
        plt.plot(range(10), [100 - x**2 for x in range(10)])
        plot.update()
    ui.timer(3.0, update_plot, once=True)

ui.run()
