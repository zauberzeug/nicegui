#!/usr/bin/env python3
from dataclasses import dataclass

import draganddrop as dnd

from nicegui import ui


@dataclass
class ToDo:
    """
    Represents a to-do item.

    Attributes:
        title (str): The title of the to-do item.
    """

    title: str


def handle_drop(todo: ToDo, location: str):
    """
    Handle the drop event for a ToDo object.

    This function is responsible for handling the drop event when a ToDo object is moved to a new location.
    It displays a notification message indicating the new location of the ToDo object.

    Parameters:
    - todo (ToDo): The ToDo object that was dropped.
    - location (str): The new location of the ToDo object.

    Returns:
    - None

    Example usage:
    ```
    todo = ToDo()
    location = "In Progress"
    handle_drop(todo, location)
    ```
    """
    ui.notify(f'"{todo.title}" is now in {location}')


with ui.row():
    with dnd.column('Next', on_drop=handle_drop):
        dnd.card(ToDo('Simplify Layouting'))
        dnd.card(ToDo('Provide Deployment'))
    with dnd.column('Doing', on_drop=handle_drop):
        dnd.card(ToDo('Improve Documentation'))
    with dnd.column('Done', on_drop=handle_drop):
        dnd.card(ToDo('Invent NiceGUI'))
        dnd.card(ToDo('Test in own Projects'))
        dnd.card(ToDo('Publish as Open Source'))
        dnd.card(ToDo('Release Native-Mode'))

ui.run()
