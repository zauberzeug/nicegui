#!/usr/bin/env python3
from nice_gui import ui
from datetime import datetime
from matplotlib import pyplot as plt
import random

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
        time = ui.label()
        ui.timer(0.1, lambda: time.set_text(datetime.now().strftime("%X")))

with ui.card():
    ui.label('Matplotlib', 'h5')
    with ui.plot(close=False) as plot:
        plt.title('Some plot')
        plt.plot(range(10), [x**2 for x in range(10)])
        x, y, colors, areas, scatter = [], [], [], [], None

    def update_plot():
        global x, y, colors, areas, scatter
        n = 20
        with plot:
            plt.title('Some plot with updates')
            x = [*x, 10 * random.triangular()][-n:]
            y = [*y, 100 * random.gauss(0.5, 0.25)][-n:]
            colors = [*colors, random.randint(1, 4)][-n:]
            areas = [*areas, random.randint(10, 30)**2][-n:]
            if scatter is not None:
                scatter.remove()
            scatter = plt.scatter(x, y, s=areas, c=colors, alpha=0.85)
    ui.timer(1.0, update_plot)

ui.run()
