# NiceGUI

<img src="https://raw.githubusercontent.com/zauberzeug/nicegui/main/sceenshots/ui-elements.png" width="300" align="right">

NiceGUI is an easy-to-use, Python-based UI framework, which renders to the web browser.
You can create buttons, dialogs, markdown, 3D scenes, plots and much more.

It was designed to be used for micro web apps, dashboards, robotics projects, smart home solutions and similar use cases.
It is also helpful for development, for example when tweaking/configuring a machine learning algorithm or tuning motor controllers.

## Features

- browser-based graphical user interface
- shared state between multiple browser windows
- implicit reload on code change
- standard GUI elements like label, button, checkbox, switch, slider, input, file upload, ...
- simple grouping with rows, columns, cards and dialogs
- general-purpose HTML and markdown elements
- powerful elements to plot graphs, render 3D scenes and get steering events via virtual joysticks
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

The GUI is now available through http://localhost:8080/ in your browser.
Note: The script will automatically reload the page when you modify the code.

Full documentation can be found at [https://nicegui.io](https://nicegui.io).

## Configuration

You can call `ui.run()` with optional arguments for some high-level configuration:

- `host` (default: `'0.0.0.0'`)
- `port` (default: `8080`)
- `title` (default: `'NiceGUI'`)
- `favicon` (default: `'favicon.ico'`)
- `reload`: automatically reload the ui on file changes (default: `True`)
- `show`: automatically open the ui in a browser tab (default: `True`)
- `uvicorn_logging_level`: logging level for uvicorn server (default: `'warning'`)
- `interactive`: used internally when run in interactive Python shell (default: `False`)
- `main_page_classes`: configure Quasar classes of main page (default: `q-ma-md column items-start`)

## Docker

Use the [multi-arch docker image](https://hub.docker.com/repository/docker/zauberzeug/nicegui) for pain-free installation:

```bash
docker run --rm -p 8888:8080 -v $(pwd)/my_script.py:/app/main.py -it zauberzeug/nicegui:latest
```

This will start the server at http://localhost:8888 with code from `my_script.py` within the current directory.
Code modification triggers an automatic reload.

## Why?

We like [Streamlit](https://streamlit.io/) but find it does [too much magic when it comes to state handling](https://github.com/zauberzeug/nicegui/issues/1#issuecomment-847413651).
In search for an alternative nice library to write simple graphical user interfaces in Python we discovered [justpy](https://justpy.io/).
While too "low-level HTML" for our daily usage it provides a great basis for "NiceGUI".

## API

The API reference is hosted at [https://nicegui.io](https://nicegui.io) and is [implemented with NiceGUI itself](https://github.com/zauberzeug/nicegui/blob/main/main.py).
You may also have a look at [examples.py](https://github.com/zauberzeug/nicegui/tree/main/examples.py) for more demonstrations of what you can do with NiceGUI.
