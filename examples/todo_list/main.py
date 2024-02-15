#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Callable, List

from nicegui import ui


@dataclass
class TodoItem:
    """
    Represents a todo item.

    Attributes:
        name (str): The name of the todo item.
        done (bool, optional): Indicates whether the todo item is done or not. Defaults to False.
    """
    name: str
    done: bool = False


@dataclass
class ToDoList:
    """
    Represents a to-do list.

    Attributes:
        title (str): The title of the to-do list.
        on_change (Callable): A callback function to be called whenever the list changes.
        items (List[TodoItem]): The list of to-do items.

    Methods:
        add(name: str, done: bool = False) -> None:
            Adds a new to-do item to the list.
        
        remove(item: TodoItem) -> None:
            Removes a to-do item from the list.
    """

    title: str
    on_change: Callable
    items: List[TodoItem] = field(default_factory=list)

    def add(self, name: str, done: bool = False) -> None:
        """
        Adds a new to-do item to the list.

        Args:
            name (str): The name of the to-do item.
            done (bool, optional): Whether the item is already done. Defaults to False.
        """
        self.items.append(TodoItem(name, done))
        self.on_change()

    def remove(self, item: TodoItem) -> None:
        """
        Removes a to-do item from the list.

        Args:
            item (TodoItem): The to-do item to be removed.
        """
        self.items.remove(item)
        self.on_change()


@ui.refreshable
def todo_ui():
    """
    Renders a todo list user interface.

    This function displays a todo list user interface using the NiceGUI library. It shows the progress of completed
    tasks, the number of completed and remaining tasks, and allows the user to mark tasks as done or delete them.

    Usage:
        - Call this function to render the todo list UI.

    Returns:
        None
    """
    if not todos.items:
        ui.label('List is empty.').classes('mx-auto')
        return
    ui.linear_progress(sum(item.done for item in todos.items) / len(todos.items), show_value=False)
    with ui.row().classes('justify-center w-full'):
        ui.label(f'Completed: {sum(item.done for item in todos.items)}')
        ui.label(f'Remaining: {sum(not item.done for item in todos.items)}')
    for item in todos.items:
        with ui.row().classes('items-center'):
            ui.checkbox(value=item.done, on_change=todo_ui.refresh).bind_value(item, 'done')
            ui.input(value=item.name).classes('flex-grow').bind_value(item, 'name')
            ui.button(on_click=lambda item=item: todos.remove(item), icon='delete').props('flat fab-mini color=grey')


todos = ToDoList('My Weekend', on_change=todo_ui.refresh)
todos.add('Order pizza', done=True)
todos.add('New NiceGUI Release')
todos.add('Clean the house')
todos.add('Call mom')

with ui.card().classes('w-80 items-stretch'):
    ui.label().bind_text_from(todos, 'title').classes('text-semibold text-2xl')
    todo_ui()
    add_input = ui.input('New item').classes('mx-12')
    add_input.on('keydown.enter', lambda: (todos.add(add_input.value), add_input.set_value('')))

ui.run()
