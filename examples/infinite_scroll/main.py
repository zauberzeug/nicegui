#!/usr/bin/env python3
import time

from nicegui import ui


@ui.page('/')
async def page():
    async def check():
        if await ui.run_javascript('window.pageYOffset >= document.body.offsetHeight - 2 * window.innerHeight'):
            ui.image(f'https://picsum.photos/640/360?{time.time()}')
    await ui.context.get_client().connected()
    ui.timer(0.1, check)


ui.run()
