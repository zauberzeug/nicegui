# NiceGUI

<img src="https://raw.githubusercontent.com/zauberzeug/nicegui/main/sceenshots/ui-elements.png" width="300" align="right">

We like [Streamlit](https://streamlit.io/) but find it does to much magic when it comes to state handling. In search for an alernative nice library to write simple graphical user interfaces in Python we discovered [justpy](https://justpy.io/). While too "low-level-html" for our daily usage it provides a great basis for our shot at a "NiceGUI".

## Features

- browser-based GUI
- implicit reload on code change
- clean set of GUI elements (label, button, checkbox, switch, slider, input, ...)
- simple grouping with rows, columns and cards
- built-in timer to refresh data in intervals (even every 10 ms)
- straight-forward data bindings to write even less code

## Install

```bash
python3 -m pip install nicegui
```

## Usage

Write your nice GUI in a file `main.py`:

```python
from nicegui import ui

ui.label('Hello NiceGUI!')
ui.button('BUTTON', on_click=lambda: print('button was pressed'))
```

Launch it with:

```bash
python3 main.py
```

Note: The script will automatically reload the GUI if you modify your code.

## API

See [main.py](https://github.com/zauberzeug/nicegui/tree/main/main.py) for an extensive example what you can do with NiceGUI.

### Interactive Elements

<img src="https://raw.githubusercontent.com/zauberzeug/nicegui/main/sceenshots/demo-boolean-interaction.gif" width="100" align="right">

`Button`, `Checkbox` and `Switch` require a name which is displayed as their label and a callback. The callback can have an optional `event` parameter which provides informations like sender and value:

```python
ui.button('Button', on_click=lambda: result.set_text('Button: pressed'))
ui.checkbox('Checkbox', on_change=lambda e: result.set_text(f'checkbox: {e.value}'))
ui.switch('Switch', on_change=lambda e: result.set_text(f'switch: {e.value}'))

result = ui.label('please interact', typography='bold')
```

<img src="https://raw.githubusercontent.com/zauberzeug/nicegui/main/sceenshots/demo-input.gif" width="200" align="right">

Use `ui.input` to receive text and `ui.number` for explicit number input.

```python
ui.input(label='Text', on_change=lambda e: result.set_text(e.value))
ui.number(label='Number', format='%.2f', on_change=lambda e: result.set_text(e.value))

result = ui.label('please type', typography='bold')
```

Pre-fill `ui.input` with the `text` property and `ui.number` with `value`.

### Styling & Design

NiceGUI use the [Quasar Framework](https://quasar.dev/) and hence has their full design power. Each NiceGUI element provides a `design` property which content is passed [as props the Quasar component](https://justpy.io/quasar_tutorial/introduction/#props-of-quasar-components):

<img src="https://raw.githubusercontent.com/zauberzeug/nicegui/main/sceenshots/demo-design.gif" width="200" align="right">

```python
ui.radio(['x', 'y', 'z'], design='inline color=green')
ui.button(icon='touch_app', design='outline round')
```

Have a look at [the Quasar documentation](https://quasar.dev/vue-components/button#design) for all styling "props".

### Timer

One major drive behind the creation of NiceGUI was the necessity to have an simple approach to update the interface
in regular intervals. For example to show a graph with incomming measurements (see plots below):

```python
clock = ui.label()
ui.timer(interval=0.1, callback=lambda: clock.set_text(datetime.now().strftime("%X")))
```

With an optional third parameter `once=True` the `callback` is once executed after an delay specified by `interval`. Otherwise the `callback` is run repeatedly.

### Plots

<img src="https://raw.githubusercontent.com/zauberzeug/nicegui/main/sceenshots/demo-plot.png" width="300" align="right">
To render a simple plot you create a new context and call the neccessary [Matplotlib](https://matplotlib.org/) functions:

```python
from nicegui import ui
from matplotlib import pyplot as plt
import numpy as np

with ui.plot():
    x = np.linspace(0.0, 5.0)
    y = np.cos(2 * np.pi * x) * np.exp(-x)
    plt.plot(x, y, '-')
    plt.xlabel('time (s)')
    plt.ylabel('Damped oscillation')
```

To update a plot in regular intervals, have look at [main.py](https://github.com/zauberzeug/nicegui/tree/main/main.py).

<img src="https://raw.githubusercontent.com/zauberzeug/nicegui/main/sceenshots/demo-live-plot.gif" width="300" align="right">

To simplify live updating line plots even more, NiceGUI provides `ui.line_plot` with useful parameters and a `push` method:

```python
lines = ui.line_plot(n=2, limit=20).with_legend(['sin', 'cos'], loc='upper center', ncol=2)
ui.timer(0.1, lambda: lines.push([datetime.now()], [
    [np.sin(datetime.now().timestamp()) + 0.02 * np.random.randn()],
    [np.cos(datetime.now().timestamp()) + 0.02 * np.random.randn()],
]))
```
