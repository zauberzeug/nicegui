#!/usr/bin/env python3
from typing import List

import httpx

from nicegui import events, ui


class Lightbox:
    """A thumbnail gallery where each image can be clicked to enlarge.
    Inspired by https://lokeshdhakar.com/projects/lightbox2/.

    Attributes:
        dialog (ui.dialog): The dialog that contains the lightbox UI.
        large_image (ui.image): The image element used to display the enlarged image.
        image_list (List[str]): A list of URLs of the original images.

    Methods:
        __init__(): Initializes the Lightbox class.
        add_image(thumb_url: str, orig_url: str) -> ui.image: Adds a thumbnail image to the UI and makes it clickable to enlarge.
        _handle_key(event_args: events.KeyEventArguments) -> None: Handles keyboard events for navigating between images.
        _open(url: str) -> None: Opens the dialog and displays the enlarged image.

    Usage:
        # Create an instance of Lightbox
        lightbox = Lightbox()

        # Add thumbnail images to the lightbox
        lightbox.add_image(thumb_url, orig_url)

        # Handle keyboard events for navigating between images
        lightbox._handle_key(event_args)

        # Open the dialog and display the enlarged image
        lightbox._open(url)
    """

    def __init__(self) -> None:
        with ui.dialog().props('maximized').classes('bg-black') as self.dialog:
            ui.keyboard(self._handle_key)
            self.large_image = ui.image().props('no-spinner fit=scale-down')
        self.image_list: List[str] = []

    def add_image(self, thumb_url: str, orig_url: str) -> ui.image:
        """
        Add a thumbnail image to the UI and make it clickable to enlarge.

        Parameters:
            thumb_url (str): The URL of the thumbnail image.
            orig_url (str): The URL of the original image.

        Returns:
            ui.image: The thumbnail image widget.

        Usage:
            To add a thumbnail image to the UI and make it clickable to enlarge,
            call this method with the URL of the thumbnail image and the URL of
            the original image. The method will append the original image URL to
            the image_list and return the thumbnail image widget.

            Example:
            thumb = add_image('https://example.com/thumbnail.jpg', 'https://example.com/original.jpg')
        """
        self.image_list.append(orig_url)
        with ui.button(on_click=lambda: self._open(orig_url)).props('flat dense square'):
            return ui.image(thumb_url)

    def _handle_key(self, event_args: events.KeyEventArguments) -> None:
            """
            Handles key events for the lightbox dialog.

            Args:
                event_args (events.KeyEventArguments): The event arguments containing information about the key event.

            Returns:
                None

            Raises:
                None

            Usage:
                This method is called internally by the lightbox dialog to handle key events. It performs the following actions:
                - If the key event is not a keydown event, the method returns without performing any action.
                - If the Escape key is pressed, the dialog is closed.
                - If the left arrow key is pressed and there is a previous image in the image list, the method opens the previous image.
                - If the right arrow key is pressed and there is a next image in the image list, the method opens the next image.
            """
            if not event_args.action.keydown:
                return
            if event_args.key.escape:
                self.dialog.close()
            image_index = self.image_list.index(self.large_image.source)
            if event_args.key.arrow_left and image_index > 0:
                self._open(self.image_list[image_index - 1])
            if event_args.key.arrow_right and image_index < len(self.image_list) - 1:
                self._open(self.image_list[image_index + 1])

    def _open(self, url: str) -> None:
        """
        Opens a lightbox dialog with a large image from the given URL.

        Parameters:
            url (str): The URL of the image to be displayed in the lightbox.

        Returns:
            None

        This method sets the source of the large image in the lightbox to the given URL and opens the dialog.
        The lightbox dialog is a graphical user interface component that displays a larger version of an image
        in an overlay window. It provides a convenient way to view images in a larger size without leaving the
        current context.

        Example usage:
            _open("https://example.com/image.jpg")
        """
        self.large_image.set_source(url)
        self.dialog.open()


@ui.page('/')
async def page():
    """
    This function creates a web page that displays a collection of images in a lightbox.

    The function performs the following steps:
    1. Creates a Lightbox object to hold the images.
    2. Sends an asynchronous HTTP GET request to retrieve a list of images from 'https://picsum.photos'.
    3. Constructs the image URLs using the image IDs obtained from the response.
    4. Adds each image to the lightbox with its thumbnail URL and original URL.
    5. Renders the images on the web page using the 'ui.row' function.

    Usage:
    1. Import the necessary modules and classes.
    2. Call the 'page' function in an asynchronous context to create the web page.

    Example:
    ```python
    import httpx
    from nicegui import ui, Lightbox

    async def main():
        await page()

    if __name__ == '__main__':
        import asyncio
        asyncio.run(main())
    ```
    """
    lightbox = Lightbox()
    async with httpx.AsyncClient() as client:  # using async httpx instead of sync requests to avoid blocking the event loop
        images = await client.get('https://picsum.photos/v2/list?page=4&limit=30')
    with ui.row().classes('w-full'):
        for image in images.json():  # picsum returns a list of images as json data
            # we can use the image ID to construct the image URLs
            image_base_url = f'https://picsum.photos/id/{image["id"]}'
            # the lightbox allows us to add images which can be opened in a full screen dialog
            lightbox.add_image(
                thumb_url=f'{image_base_url}/300/200',
                orig_url=f'{image_base_url}/{image["width"]}/{image["height"]}',
            ).classes('w-[300px] h-[200px]')

ui.run()
