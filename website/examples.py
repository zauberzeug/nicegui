from dataclasses import dataclass, field
from pathlib import Path
from typing import List

PATH = Path(__file__).parent.parent / 'examples'


@dataclass
class Example:
    title: str
    description: str
    url: str = field(init=False)

    def __post_init__(self) -> None:
        """Post-initialization hook."""
        name = self.title.lower().replace(' ', '_')
        content = [p for p in (PATH / name).glob('*') if not p.name.startswith(('__pycache__', '.', 'test_'))]
        filename = 'main.py' if len(content) == 1 else ''
        self.url = f'https://github.com/zauberzeug/nicegui/tree/main/examples/{name}/{filename}'


examples: List[Example] = [
    Example('Slideshow', 'implements a keyboard-controlled image slideshow'),
    Example('Authentication', 'shows how to use sessions to build a login screen'),
    Example('Modularization', 'provides an example of how to modularize your application into multiple files and reuse code'),
    Example('FastAPI', 'illustrates the integration of NiceGUI with an existing FastAPI application'),
    Example('AI Interface',
            'utilizes the [replicate](https://replicate.com) library to perform voice-to-text transcription and generate images from prompts with Stable Diffusion'),
    Example('3D Scene', 'creates a webGL view and loads an STL mesh illuminated with a spotlight'),
    Example('Custom Vue Component', 'shows how to write and integrate a custom Vue component'),
    Example('Image Mask Overlay', 'shows how to overlay an image with a mask'),
    Example('Infinite Scroll', 'presents an infinitely scrolling image gallery'),
    Example('OpenCV Webcam', 'uses OpenCV to capture images from a webcam'),
    Example('SVG Clock', 'displays an analog clock by updating an SVG with `ui.timer`'),
    Example('Progress', 'demonstrates a progress bar for heavy computations'),
    Example('Global Worker', 'demonstrates a global worker for heavy computations with progress feedback'),
    Example('NGINX Subpath', 'shows the setup to serve an app behind a reverse proxy subpath'),
    Example('Script Executor', 'executes scripts on selection and displays the output'),
    Example('Local File Picker', 'demonstrates a dialog for selecting files locally on the server'),
    Example('Search as you type',
            'using public API of [thecocktaildb.com](https://www.thecocktaildb.com/) to search for cocktails'),
    Example('Menu and Tabs', 'uses Quasar to create foldable menu and tabs inside a header bar'),
    Example('Todo list', 'shows a simple todo list with checkboxes and text input'),
    Example('Trello Cards', 'shows Trello-like cards that can be dragged and dropped into columns'),
    Example('Slots', 'shows how to use scoped slots to customize Quasar elements'),
    Example('Table and slots', 'shows how to use component slots in a table'),
    Example('Single Page App', 'navigate without reloading the page'),
    Example('Chat App', 'a simple chat app'),
    Example('Chat with AI', 'a simple chat app with AI'),
    Example('SQLite Database', 'CRUD operations on a SQLite database with async-support through Tortoise ORM'),
    Example('Pandas DataFrame', 'displays an editable [pandas](https://pandas.pydata.org) DataFrame'),
    Example('Lightbox', 'a thumbnail gallery where each image can be clicked to enlarge'),
    Example('ROS2', 'Using NiceGUI as web interface for a ROS2 robot'),
    Example('Docker Image',
            'use the official [zauberzeug/nicegui](https://hub.docker.com/r/zauberzeug/nicegui) docker image'),
    Example('Download Text as File', 'providing in-memory data like strings as file download'),
    Example('Generate PDF', 'create an SVG preview and PDF download from input form elements'),
    Example('Custom Binding', 'create a custom binding for a label with a bindable background color'),
    Example('Descope Auth', 'login form and user profile using [Descope](https://descope.com)'),
    Example('Editable table', 'editable table allowing to add, edit, delete rows'),
    Example('Editable AG Grid', 'editable AG Grid allowing to add, edit, delete rows'),
    Example('FullCalendar', 'show an interactive calendar using the [FullCalendar library](https://fullcalendar.io/)'),
    Example('Pytests', 'test a NiceGUI app with pytest'),
    Example('Pyserial', 'communicate with a serial device'),
    Example('Webserial', 'communicate with a serial device using the WebSerial API'),
    Example('Websockets', 'use [websockets library](https://websockets.readthedocs.io/) to start a websocket server'),
    Example('Audio Recorder', 'Record audio, play it back or download it'),
    Example('ZeroMQ', 'Simple ZeroMQ PUSH/PULL server and client'),
    Example('NGINX HTTPS', 'Use NGINX to serve a NiceGUI app with HTTPS'),
    Example('Node Module Integration', 'Use NPM to add dependencies to a NiceGUI app'),
    Example('Signature Pad', 'A custom element based on [signature_pad](https://www.npmjs.com/package/signature_pad'),
    Example('OpenAI Assistant', "Using OpenAI's Assistant API with async/await"),
    Example('Redis Storage', 'Use Redis storage to share data across multiple instances behind a reverse proxy or load balancer'),
]
