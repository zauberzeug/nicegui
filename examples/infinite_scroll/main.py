#!/usr/bin/env python3
import time

from nicegui import ui


@ui.page('/')
def page():
    async def check():
        response = await ui.run_javascript('window.pageYOffset >= document.body.offsetHeight - 2 * window.innerHeight')
        if list(response.values())[0]:
            ui.image(f'https://picsum.photos/640/360?{time.time()}')
    yield
    ui.timer(0.1, check)


ui.run()
