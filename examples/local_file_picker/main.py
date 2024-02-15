#!/usr/bin/env python3
from local_file_picker import local_file_picker

from nicegui import ui


async def pick_file() -> None:
    """
    Asynchronously prompts the user to pick one or more local files.

    This function uses the `local_file_picker` function from the NiceGUI library to display a file picker dialog
    to the user. The user can select one or more files from their local file system. The function then returns
    the selected file paths as a list.

    Parameters:
        None

    Returns:
        None

    Example usage:
        await pick_file()
    """
    result = await local_file_picker('~', multiple=True)
    ui.notify(f'You chose {result}')

ui.button('Choose file', on_click=pick_file, icon='folder')

ui.run()
