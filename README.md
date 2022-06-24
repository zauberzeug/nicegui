<img src="https://raw.githubusercontent.com/zauberzeug/nicegui/main/sceenshots/ui-elements.png" width="300" align="right">

# NiceGUI

NiceGUI is an easy-to-use, Python-based UI framework, which renders to the web browser.
You can create buttons, dialogs, markdown, 3D scenes, plots and much more.

It is great for micro web apps, dashboards, robotics projects, smart home solutions and similar use cases.
You can also use it in development, for example when tweaking/configuring a machine learning algorithm or tuning motor controllers.

NiceGUI is available as [PyPI package](https://pypi.org/project/nicegui/), [Docker image](https://hub.docker.com/r/zauberzeug/nicegui) and on [GitHub](https://github.com/zauberzeug/nicegui).

[![PyPI version](https://badge.fury.io/py/nicegui.svg)](https://pypi.org/project/nicegui/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/nicegui)](https://pypi.org/project/nicegui/)
[![Docker Pulls](https://img.shields.io/docker/pulls/zauberzeug/nicegui)](https://hub.docker.com/r/zauberzeug/nicegui)<br />
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/zauberzeug/nicegui)](https://github.com/zauberzeug/nicegui/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/zauberzeug/nicegui)](https://github.com/zauberzeug/nicegui/issues)
[![GitHub forks](https://img.shields.io/github/forks/zauberzeug/nicegui)](https://github.com/zauberzeug/nicegui/network)
[![GitHub stars](https://img.shields.io/github/stars/zauberzeug/nicegui)](https://github.com/zauberzeug/nicegui/stargazers)
[![GitHub license](https://img.shields.io/github/license/zauberzeug/nicegui)](https://github.com/zauberzeug/nicegui/blob/main/LICENSE)

## Features

- browser-based graphical user interface
- shared state between multiple browser windows
- implicit reload on code change
- standard GUI elements like label, button, checkbox, switch, slider, input, file upload, ...
- simple grouping with rows, columns, cards and dialogs
- general-purpose HTML and markdown elements
- powerful high-level elements to
  - plot graphs and charts,
  - render 3D scenes,
  - get steering events via virtual joysticks
  - annotate images
- built-in timer to refresh data in intervals (even every 10 ms)
- straight-forward data binding to write even less code
- notifications, dialogs and menus to provide state of the art user interaction
- ability to add custom routes and data responses
- capture keyboard input for global shortcuts etc
- customize look by defining primary, secondary and accent colors

## Installation

```bash
python3 -m pip install nicegui
```

## Usage

Write your nice GUI in a file `main.py`:

```python
from nicegui import ui

ui.label('Hello NiceGUI!')
ui.button('BUTTON', on_click=lambda: ui.notify('button was pressed'))

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

You can call `ui.run()` with optional arguments:

- `host` (default: `'0.0.0.0'`)
- `port` (default: `8080`)
- `title` (default: `'NiceGUI'`)
- `favicon` (default: `'favicon.ico'`)
- `dark`: whether to use Quasar's dark mode (default: `False`, use `None` for "auto" mode)
- `reload`: automatically reload the ui on file changes (default: `True`)
- `show`: automatically open the ui in a browser tab (default: `True`)
- `uvicorn_logging_level`: logging level for uvicorn server (default: `'warning'`)
- `uvicorn_reload_dirs`: string with comma-separated list for directories to be monitored (default is current working directory only)
- `uvicorn_reload_includes`: string with comma-separated list of glob-patterns which trigger reload on modification (default: `'.py'`)
- `uvicorn_reload_excludes`: string with comma-separated list of glob-patterns which should be ignored for reload (default: `'.*, .py[cod], .sw.*, ~*'`)
- `main_page_classes`: configure Quasar classes of main page (default: `'q-ma-md column items-start'`)
- `binding_refresh_interval`: time between binding updates (default: `0.1` seconds, bigger is more cpu friendly)
- `exclude`: comma-separated string to exclude libraries (with corresponding elements) to save bandwidth and/or startup time:
  - "aggrid" (`ui.table`)
  - "colors" (`ui.colors`)
  - "custom_example" (`ui.custom_example`)
  - "highcharts" (`ui.chart`)
  - "interactive_image" (`ui.interactive_image`)
  - "keyboard" (`ui.keyboard`)
  - "log" (`ui.log`)
  - "matplotlib" (`ui.plot` and `ui.line_plot`)
  - "nipple" (`ui.joystick`)
  - "three" (`ui.scene`)
- `interactive`: used internally when run in interactive Python shell (default: `False`)

The environment variables `HOST` and `PORT` can also be used to configure NiceGUI.

## Docker

You can use our [multi-arch Docker image](https://hub.docker.com/repository/docker/zauberzeug/nicegui) for pain-free installation:

```bash
docker run --rm -p 8888:8080 -v $(pwd):/app/ -it zauberzeug/nicegui:latest
```

This will start the server at http://localhost:8888 with the code from your current directory.
The file containing your `ui.run(port=8080, ...)` command must be named `main.py`.
Code modification triggers an automatic reload.

## Why?

We like [Streamlit](https://streamlit.io/) but find it does [too much magic when it comes to state handling](https://github.com/zauberzeug/nicegui/issues/1#issuecomment-847413651).
In search for an alternative nice library to write simple graphical user interfaces in Python we discovered [justpy](https://justpy.io/).
While too "low-level HTML" for our daily usage it provides a great basis for "NiceGUI".

## API

The API reference is hosted at [https://nicegui.io](https://nicegui.io) and is [implemented with NiceGUI itself](https://github.com/zauberzeug/nicegui/blob/main/main.py).
You may also have a look at [examples.py](https://github.com/zauberzeug/nicegui/tree/main/examples.py) for more demonstrations of what you can do with NiceGUI.

## Abstraction

NiceGUI is based on [JustPy](https://justpy.io/) which is based on the ASGI framework [Starlette](https://www.starlette.io/) and the ASGI webserver [Uvicorn](https://www.uvicorn.org/).

## Deployment

To deploy your NiceGUI app, you will need to execute your `main.py` (or whichever file contains your `ui.run(...)`) on your server infrastructure.
You can either install the [NiceGUI python package via pip](https://pypi.org/project/nicegui/) on the server or use our [pre-built Docker image](https://hub.docker.com/r/zauberzeug/nicegui) which contains all necessary dependencies.
For example you can use this `docker run` command to start the script `main.py` in the current directory on port 80:

```bash
docker run -p 80:8080 -v $(pwd)/:/app/ -d --restart always zauberzeug/nicegui:latest
```

The example assumes `main.py` uses the port 8080 in the `ui.run` command (which is the default).
The `--restart always` makes sure the container is restarted if the app crashes or the server reboots.
Of course this can also be written in a docker compose file:

```yaml
nicegui:
  image: zauberzeug/nicegui:latest
  restart: always
  ports:
    - 80:8080
  volumes:
    - ./:/app/
```

While it is possible to provide SSL certificates directly through NiceGUI (using [JustPy config](https://justpy.io/reference/configuration/)) we suggest to use a reverse proxy like [Traefik](https://doc.traefik.io/traefik/) or [NGINX](https://www.nginx.com/).
