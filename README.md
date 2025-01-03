<a href="https://nicegui.io/#about">
  <img src="https://raw.githubusercontent.com/zauberzeug/nicegui/main/screenshot.png"
    width="200" align="right" alt="Try online!" />
</a>

# NiceGUI

NiceGUI is an easy-to-use, Python-based UI framework, which shows up in your web browser.
You can create buttons, dialogs, Markdown, 3D scenes, plots and much more.

It is great for micro web apps, dashboards, robotics projects, smart home solutions and similar use cases.
You can also use it in development, for example when tweaking/configuring a machine learning algorithm or tuning motor controllers.

NiceGUI is available as [PyPI package](https://pypi.org/project/nicegui/), [Docker image](https://hub.docker.com/r/zauberzeug/nicegui) and on [conda-forge](https://anaconda.org/conda-forge/nicegui) as well as [GitHub](https://github.com/zauberzeug/nicegui).

[![PyPI](https://img.shields.io/pypi/v/nicegui?color=dark-green)](https://pypi.org/project/nicegui/)
[![PyPI downloads](https://img.shields.io/pypi/dm/nicegui?color=dark-green)](https://pypi.org/project/nicegui/)
[![Conda version](https://img.shields.io/conda/v/conda-forge/nicegui?color=green&label=conda-forge)](https://anaconda.org/conda-forge/nicegui)
[![Conda downloads](https://img.shields.io/conda/dn/conda-forge/nicegui?color=green&label=downloads)](https://anaconda.org/conda-forge/nicegui)
[![Docker pulls](https://img.shields.io/docker/pulls/zauberzeug/nicegui)](https://hub.docker.com/r/zauberzeug/nicegui)<br />
[![GitHub license](https://img.shields.io/github/license/zauberzeug/nicegui?color=orange)](https://github.com/zauberzeug/nicegui/blob/main/LICENSE)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/zauberzeug/nicegui)](https://github.com/zauberzeug/nicegui/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/zauberzeug/nicegui?color=blue)](https://github.com/zauberzeug/nicegui/issues)
[![GitHub forks](https://img.shields.io/github/forks/zauberzeug/nicegui)](https://github.com/zauberzeug/nicegui/network)
[![GitHub stars](https://img.shields.io/github/stars/zauberzeug/nicegui)](https://github.com/zauberzeug/nicegui/stargazers)

## Features

- browser-based graphical user interface
- implicit reload on code change
- acts as webserver (accessed by the browser) or in native mode (eg. desktop window)
- standard GUI elements like label, button, checkbox, switch, slider, input, file upload, ...
- simple grouping with rows, columns, cards and dialogs
- general-purpose HTML and Markdown elements
- powerful high-level elements to
  - plot graphs and charts,
  - render 3D scenes,
  - get steering events via virtual joysticks
  - annotate and overlay images
  - interact with tables
  - navigate foldable tree structures
  - embed video and audio files
- built-in timer to refresh data in intervals (even every 10 ms)
- straight-forward data binding and refreshable functions to write even less code
- notifications, dialogs and menus to provide state of the art user interaction
- shared and individual web pages
- easy-to-use per-user and general persistence
- ability to add custom routes and data responses
- capture keyboard input for global shortcuts etc.
- customize look by defining primary, secondary and accent colors
- live-cycle events and session data
- runs in Jupyter Notebooks and allows Python's interactive mode
- auto-complete support for Tailwind CSS
- SVG, Base64 and emoji favicon support
- testing framework based on pytest

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

The documentation is hosted at [https://nicegui.io/documentation](https://nicegui.io/documentation) and provides plenty of live demos.
The whole content of [https://nicegui.io](https://nicegui.io) is [implemented with NiceGUI itself](https://github.com/zauberzeug/nicegui/blob/main/main.py)
and can be started locally with `docker run -p 8080:8080 zauberzeug/nicegui` or by executing `main.py` from this repository.

You may also have a look at our [in-depth examples](https://github.com/zauberzeug/nicegui/tree/main/examples) of what you can do with NiceGUI.
In our wiki we have a list of great [NiceGUI projects from the community](https://github.com/zauberzeug/nicegui/wiki#community-projects), a section with [Tutorials](https://github.com/zauberzeug/nicegui/wiki#tutorials), a growing list of [FAQs](https://github.com/zauberzeug/nicegui/wiki/FAQs) and [some strategies for using ChatGPT / LLMs to get help about NiceGUI](https://github.com/zauberzeug/nicegui/wiki#chatgpt).

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

## Sponsors

Maintenance of this project is made possible by all the [contributors](https://github.com/zauberzeug/nicegui/graphs/contributors) and [sponsors](https://github.com/sponsors/zauberzeug).
If you would like to support this project and have your avatar or company logo appear below, please [sponsor us](https://github.com/sponsors/zauberzeug). 💖

<!-- SPONSORS -->
<p align="center">
  <a href="https://github.com/lechler-gmbh"><img src="https://github.com/lechler-gmbh.png" width="50px" alt="Lechler GmbH" /></a>
  <a href="https://github.com/Zhifeng2019"><img src="https://github.com/Zhifeng2019.png" width="50px" alt="Zhifeng" /></a>
  <a href="https://github.com/sereneturtlefox"><img src="https://github.com/sereneturtlefox.png" width="50px" alt="None" /></a>
  <a href="https://github.com/whoulden"><img src="https://github.com/whoulden.png" width="50px" alt="Wayne Houlden" /></a>
  <a href="https://github.com/digiquip"><img src="https://github.com/digiquip.png" width="50px" alt="DigiQuip AS" /></a>
</p>
<!-- SPONSORS -->

Consider this low-barrier form of contribution yourself.
Your [support](https://github.com/sponsors/zauberzeug) is much appreciated.

## Contributing

Thank you for your interest in contributing to NiceGUI! We are thrilled to have you on board and appreciate your efforts to make this project even better.

As a growing open-source project, we understand that it takes a community effort to achieve our goals. That's why we welcome all kinds of contributions, no matter how small or big they are. Whether it's adding new features, fixing bugs, improving documentation, or suggesting new ideas, we believe that every contribution counts and adds value to our project.

We have provided a detailed guide on how to contribute to NiceGUI in our [CONTRIBUTING.md](https://github.com/zauberzeug/nicegui/blob/main/CONTRIBUTING.md) file. We encourage you to read it carefully before making any contributions to ensure that your work aligns with the project's goals and standards.

If you have any questions or need help with anything, please don't hesitate to reach out to us. We are always here to support and guide you through the contribution process.

## Included Web Dependencies

See [DEPENDENCIES.md](https://github.com/zauberzeug/nicegui/blob/main/DEPENDENCIES.md) for a list of web frameworks NiceGUI depends on.
