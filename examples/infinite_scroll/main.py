#!/usr/bin/env python3
import itertools

from nicegui import ui


@ui.page('/')
async def page():
    names = itertools.cycle(['valley', 'mug', 'bench', 'drops', 'sea', 'bridge', 'night', 'birds', 'grapes', 'hikers'])

    async def check():
        try:
            if await ui.run_javascript('window.pageYOffset >= document.body.offsetHeight - 2 * window.innerHeight'):
                ui.image(f'https://nicegui.io/images/{next(names)}/640/360')
        except TimeoutError:
            pass  # the client might have disconnected
    await ui.context.client.connected()
    ui.timer(0.1, check)


ui.run()
