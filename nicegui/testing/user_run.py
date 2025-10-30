import os
from contextlib import asynccontextmanager

import httpx

from nicegui import core, ui
from nicegui.functions.download import download
from nicegui.functions.navigate import Navigate
from nicegui.functions.notify import notify
from nicegui.testing.user_plugin import User


@asynccontextmanager
async def run(ui_code):
    """A user context manager for the given `nicegui.ui` code.
    
    Example use in a plain pytest function without user plugin use:

    ```
    async def test_button_click():
        def ui_code() -> None:
            ui.button('Click me', on_click=lambda: ui.notify('Hello World!'))

        async with run(ui_code) as user:
            await user.open('/')
            await user.should_see('Click me')
            user.find(ui.button).click()
            await user.should_see('Hello World!')
    ```

    """
    try:
        # simulate user and keep NiceGUI fully headless for tests
        os.environ['NICEGUI_USER_SIMULATION'] = 'true'

        # don't spawn reloader/native window; don't open browser
        ui.run(ui_code, reload=False, native=False, show=False)

        async with core.app.router.lifespan_context(core.app):
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(core.app),
                base_url='http://test'
            ) as client:
                yield User(client)
    finally:
        os.environ.pop('NICEGUI_USER_SIMULATION', None)
        ui.navigate = Navigate()
        ui.notify = notify
        ui.download = download


