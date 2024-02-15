#!/usr/bin/env python3
import time

from nicegui import Client, ui


@ui.page('/')
async def page(client: Client):
    """
    This function represents a page in a web application that implements infinite scrolling.

    Parameters:
        client (Client): An instance of the Client class used for communication with the server.

    Returns:
        None

    Description:
        This function is an asynchronous coroutine that sets up a page with infinite scrolling functionality.
        It continuously checks the scroll position of the page and appends new images to the UI when the user
        reaches the bottom of the page.

        The function takes a single argument, `client`, which is an instance of the Client class. This client
        is used to establish a connection with the server.

        The `check` function is an inner function that is called periodically using a timer. It checks if the
        user has scrolled to the bottom of the page by comparing the scroll position (`window.pageYOffset`) with
        the total height of the page (`document.body.offsetHeight`). If the user is close to the bottom
        (within 2 times the window height), a new image is appended to the UI using the `ui.image` function.

        Example usage:
        ```
        client = Client()
        await page(client)
        ```

    """
    async def check():
        if await ui.run_javascript('window.pageYOffset >= document.body.offsetHeight - 2 * window.innerHeight'):
            ui.image(f'https://picsum.photos/640/360?{time.time()}')
    await client.connected()
    ui.timer(0.1, check)


ui.run()
