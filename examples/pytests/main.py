#!/usr/bin/env python3
from pytests.startup import startup

from nicegui import app, ui

app.on_startup(startup)

ui.run()
