<a href="http://nicegui.io/#about">
  <img src="https://raw.githubusercontent.com/zauberzeug/nicegui/main/sceenshots/ui-elements-narrow.png"
    width="200" align="right" alt="Try online!" />
</a>

# NiceGUI

NiceGUI is an easy-to-use, Python-based UI framework, which shows up in your web browser.
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
- implicit reload on code change
- standard GUI elements like label, button, checkbox, switch, slider, input, file upload, ...
- simple grouping with rows, columns, cards and dialogs
- general-purpose HTML and markdown elements
- powerful high-level elements to
  - plot graphs and charts,
  - render 3D scenes,
  - get steering events via virtual joysticks
  - annotate and overlay images
  - interact with tables
  - navigate foldable tree structures
- built-in timer to refresh data in intervals (even every 10 ms)
- straight-forward data binding to write even less code
- notifications, dialogs and menus to provide state of the art user interaction
- shared and individual web pages
- ability to add custom routes and data responses
- capture keyboard input for global shortcuts etc.
- customize look by defining primary, secondary and accent colors
- live-cycle events and session data

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
Note: NiceGUI will automatically reload the page when you modify the code.

## Documentation and Examples

The API reference is hosted at [https://nicegui.io/reference](https://nicegui.io/reference) and provides plenty of live examples.
The whole content of [https://nicegui.io](https://nicegui.io) is [implemented with NiceGUI itself](https://github.com/zauberzeug/nicegui/blob/main/main.py).

You may also have a look at [our in-depth demonstrations](https://github.com/zauberzeug/nicegui/tree/main/examples) of what you can do with NiceGUI.

## Why?

We at [Zauberzeug](https://zauberzeug.com) like [Streamlit](https://streamlit.io/)
but find it does [too much magic](https://github.com/zauberzeug/nicegui/issues/1#issuecomment-847413651) when it comes to state handling.
In search for an alternative nice library to write simple graphical user interfaces in Python we discovered [JustPy](https://justpy.io/).
Although we liked the approach, it is too "low-level HTML" for our daily usage.
But it inspired us to use [Vue](https://vuejs.org/) and [Quasar](https://quasar.dev/) for the frontend.

We have built on top of [FastAPI](https://fastapi.tiangolo.com/),
which itself is based on the ASGI framework [Starlette](https://www.starlette.io/)
and the ASGI webserver [Uvicorn](https://www.uvicorn.org/)
because of their great performance and ease of use.

## Docker

You can use our [multi-arch Docker image](https://hub.docker.com/repository/docker/zauberzeug/nicegui):

```bash
docker run --rm -p 8888:8080 -v $(pwd):/app/ -it zauberzeug/nicegui:latest
```

This will start the server at http://localhost:8888 with the code from your current directory.
The file containing your `ui.run(port=8080, ...)` command must be named `main.py`.
Code modification triggers an automatic reload.

## Deployment

To deploy your NiceGUI app, you will need to execute your `main.py` (or whichever file contains your `ui.run(...)`) on your server infrastructure.
You can either install the [NiceGUI python package via pip](https://pypi.org/project/nicegui/) on the server
or use our [pre-built Docker image](https://hub.docker.com/r/zauberzeug/nicegui) which contains all necessary dependencies (see above).
For example you can use this `docker run` command to start the script `main.py` in the current directory on port 80:

```bash
docker run -p 80:8080 -v $(pwd)/:/app/ -d --restart always zauberzeug/nicegui:latest
```

The example assumes `main.py` uses the port 8080 in the `ui.run` command (which is the default).
The `--restart always` makes sure the container is restarted if the app crashes or the server reboots.
Of course this can also be written in a Docker compose file:

```yaml
nicegui:
  image: zauberzeug/nicegui:latest
  restart: always
  ports:
    - 80:8080
  volumes:
    - ./:/app/
```

You can provide SSL certificates directly using [FastAPI](https://fastapi.tiangolo.com/deployment/https/).
In production we also like using reverse proxies like [Traefik](https://doc.traefik.io/traefik/) or [NGINX](https://www.nginx.com/) to handle these details for us.
See our [docker-compose.yml](https://github.com/zauberzeug/nicegui/blob/main/docker-compose.yml) as an example.

You may also have look at [our example for using a custom FastAPI app](https://github.com/zauberzeug/nicegui/tree/main/examples/fastapi).
This will allow you to do very flexible deployments as described in the [FastAPI documentation](https://fastapi.tiangolo.com/deployment/).
