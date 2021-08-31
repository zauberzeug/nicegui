# NiceGUI

<img src="https://raw.githubusercontent.com/zauberzeug/nicegui/main/sceenshots/ui-elements.png" width="300" align="right">

We like [Streamlit](https://streamlit.io/) but find it does [too much magic when it comes to state handling](https://github.com/zauberzeug/nicegui/issues/1#issuecomment-847413651).
In search for an alernative nice library to write simple graphical user interfaces in Python we discovered [justpy](https://justpy.io/).
While too "low-level HTML" for our daily usage it provides a great basis for "NiceGUI".

## Purpose

NiceGUI is intended to be used for small scripts and single-page user interfaces with a very limited user base.
Like smart home solutions, micro web apps or robotics projects.
It's also helpful for development, when tweaking/configuring a machine learning training or tuning motor controllers.

## Features

- browser-based graphical user interface
- shared state between multiple browser windows
- implicit reload on code change
- standard GUI elements like label, button, checkbox, switch, slider, input, file upload, ...
- simple grouping with rows, columns, cards and dialogs
- general-purpose HTML and markdown elements
- powerful elements to plot graphs, render 3D scences and get steering events via virtual joysticks
- built-in timer to refresh data in intervals (even every 10 ms)
- straight-forward data binding to write even less code
- notifications, dialogs and menus to provide state of the art user interaction

## Installation

```bash
python3 -m pip install nicegui
```

## Usage

Write your nice GUI in a file `main.py`:

```python
from nicegui import ui

ui.label('Hello NiceGUI!')
ui.button('BUTTON', on_click=lambda: print('button was pressed', flush=True))

ui.run()
```

Launch it with:

```bash
python3 main.py
```

The GUI is now avaliable through http://localhost/ in your browser.
Note: The script will automatically reload the page when you modify the code.

## Configuration

You can call `ui.run()` with optional arguments for some high-level configuration:

- `host` (default: `'0.0.0.0'`)
- `port` (default: `80`)
- `title` (default: `'NiceGUI'`)
- `favicon` (default: `'favicon.ico'`)
- `reload`: automatically reload the ui on file changes (default: `True`)
- `show`: automatically open the ui in a browser tab (default: `True`)
- `interactive`: used internally when run in interactive Python shell (default: `False`)

## Docker

Use the [multi-arch docker image](https://hub.docker.com/repository/docker/zauberzeug/nicegui) for pain-free installation:

```bash
docker run --rm -p 8888:80 -v $(pwd)/my_script.py:/app/main.py -it zauberzeug/nicegui:latest
```

This will start the server at http://localhost:8888 with code from `my_script.py` within the current directory.
Code modification triggers an automatic reload.

## API

The API reference is hosted at [https://nicegui.io](https://nicegui.io) and is [implemented with NiceGUI itself](https://github.com/zauberzeug/nicegui/blob/main/main.py).
You should also have a look at [examples.py](https://github.com/zauberzeug/nicegui/tree/main/examples.py) for an extensive demonstration of what you can do with NiceGUI.
