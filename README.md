<a href="http://nicegui.io/#about">
  <img src="sceenshots/ui-elements-narrow.png" width="200" align="right" alt="Try online!" />
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

### Interaction

- buttons, switches, sliders, inputs, ...
- notifications, dialogs and menus
- keyboard input
- on-screen joystick

### Layout

- navigation bars, tabs, panels, ...
- grouping with rows, columns and cards
- HTML and markdown elements
- flex layout by default

### Visualization

- charts, diagrams and tables
- 3D scenes
- progress bars
- built-in timer for data refresh

### Styling

- customizable color themes
- custom CSS and classes
- modern look with material design
- built-in [Tailwind](https://tailwindcss.com/) support

### Coding

- live-cycle events
- implicit reload on code change
- straight-forward data binding
- execute javascript from Python

### Foundation

- generic [Vue](https://vuejs.org/) to Python bridge
- dynamic GUI through [Quasar](https://quasar.dev/)
- content is served with [FastAPI](http://fastapi.tiangolo.com/)
- Python 3.7+

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

You may also have a look at the following examples for in-depth demonstrations of what you can do with NiceGUI:

- [Slideshow](https://github.com/zauberzeug/nicegui/tree/main/examples/slideshow/main.py):
  implements a keyboard-controlled image slideshow
- [Authentication](https://github.com/zauberzeug/nicegui/blob/main/examples/authentication/main.py):
  shows how to use sessions to build a login screen
- [Modularization](https://github.com/zauberzeug/nicegui/blob/main/examples/modularization/main.py):
  provides an example of how to modularize your application into multiple files and reuse code
- [FastAPI](https://github.com/zauberzeug/nicegui/tree/main/examples/fastapi/main.py)
  illustrates the integration of NiceGUI with an existing FastAPI application
- [Map](https://github.com/zauberzeug/nicegui/blob/main/examples/map/main.py):
  demonstrates wrapping the JavaScript library [leaflet](https://leafletjs.com/) to display a map at specific locations
- [AI User Interface](https://github.com/zauberzeug/nicegui/blob/main/examples/ai_interface/main.py):
  utilizes the [replicate](https://replicate.com) library to perform voice-to-text transcription and generate images from prompts with Stable Diffusion
- [3D Scene](https://github.com/zauberzeug/nicegui/blob/main/examples/3d_scene/main.py):
  creates a webGL view and loads an STL mesh illuminated with a spotlight
- [Custom Vue Component](https://github.com/zauberzeug/nicegui/blob/main/examples/custom_vue_component/main.py)
  shows how to write and integrate a custom Vue component
- [Image Mask Overlay](https://github.com/zauberzeug/nicegui/blob/main/examples/image_mask_overlay/main.py):
  shows how to overlay an image with a mask
- [Infinite Scroll](https://github.com/zauberzeug/nicegui/blob/main/examples/infinite_scroll/main.py):
  presents an infinitely scrolling image gallery

## Why?

We like [Streamlit](https://streamlit.io/)
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
