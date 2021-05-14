# Nice GUI

<img src="sceenshots/ui-elements.png?raw=true" width="300" align="right">

We like [Streamlit](https://streamlit.io/) but find it does to much magic when it comes to state handling. In search for an alernative nice library to write simple graphical user interfaces in Python we discovered [justpy](https://justpy.io/). While to "low-level-html" for our daily usage it provides a great basis for our shot at a "Nice GUI".


## Features

- implicit code reloading
- live plot updates (see below)
- clean set of gui elements (label, button, checkbox, switch, slider, input, ...)
- simple grouping with rows, columns and cards
- buildin timer to refresh data in intervals (even every 10 ms)

## Usage

Write your nice GUI in a file `main.py`:

```python
from nice_gui import ui

ui.label('Hello Nice GUI!')
ui.button('BUTTON', on_click: lambda: print('button was pressed'))
```

Launch it with:

```bash
python3 main.py
```

Note: the script will automatically reload the GUI if you modify your code.

## API

See [main.py](https://github.com/zauberzeug/nice_gui/blob/main/main.py) for an example of all API calls you can make with Nice GUI.

## Plots

<img src="sceenshots/live-plot.gif?raw=true" width="400" align="right">

```python
lines = ui.line_plot(n=2, limit=20).with_legend(['sin', 'cos'], loc='upper center', ncol=2)
ui.timer(1.0, lambda: lines.push([datetime.now()], [
    [np.sin(datetime.now().timestamp()) + 0.02 * np.random.randn()],
    [np.cos(datetime.now().timestamp()) + 0.02 * np.random.randn()],
]))
```
