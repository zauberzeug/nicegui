# NiceGUI

<img src="https://raw.githubusercontent.com/zauberzeug/nicegui/main/sceenshots/ui-elements.png" width="300" align="right">

We like [Streamlit](https://streamlit.io/) but find it does to much magic when it comes to state handling. In search for an alernative nice library to write simple graphical user interfaces in Python we discovered [justpy](https://justpy.io/). While too "low-level-html" for our daily usage it provides a great basis for "NiceGUI".

## Purpose

NiceGUI is intended to be used for small scripts and user interfaces with a very limited user base. Custom "Smart-Home Control" solutions or "Robotics" for example. It's also helpful for development like tweaking/configuring a machine learning training or tuning motor controllers.

## Features

- browser-based GUI
- shared state between multiple browser windows
- implicit reload on code change
- clean set of GUI elements (label, button, checkbox, switch, slider, input, ...)
- simple grouping with rows, columns and cards
- genral-purpose html and markdown elements
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

API Reference is hosted at [https://nicegui.io](https://nicegui.io). Also have a look at [examples.py](https://github.com/zauberzeug/nicegui/tree/main/examples.py) for an extensive demonstration what you can do with NiceGUI.
