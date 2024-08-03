#!/usr/bin/env python3
from app.startup import startup

from nicegui import app, ui

app.on_startup(startup)

ui.run()
