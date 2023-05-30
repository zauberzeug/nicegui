#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Callable

from nicegui import ui


@dataclass
class TodoItem:
    name: str
    on_change: Callable
    done: bool = False

    def toggle(self) -> None:
        self.done = not self.done

    def set_name(self, new_name: str) -> None:
        self.name = new_name

    def __setattr__(self, name, value) -> None:
        super().__setattr__(name, value)
        if hasattr(self, 'on_change'):
            self.on_change()


class ToDoList:

    def __init__(self, title: str, on_change: Callable):
        self.title = title
        self.items = []
        self.on_change: Callable = on_change

    def add(self, name: str, done: bool = False) -> None:
        self.items.append(TodoItem(name, self.on_change, done))
        self.on_change()

    def remove(self, item: TodoItem) -> None:
        self.items.remove(item)
        self.on_change()


@ui.refreshable
def todo_ui():
    if not todos.items:
        ui.label('List is empty.').classes('mx-auto')
        return
    ui.linear_progress(sum(item.done for item in todos.items) / len(todos.items), show_value=False)
    with ui.row().classes('justify-center w-full'):
        ui.label(f'Completed: {sum(item.done for item in todos.items)}')
        ui.label(f'Remaining: {sum(not item.done for item in todos.items)}')
    for item in todos.items:
        with ui.row().classes('items-center'):
            ui.checkbox(value=item.done, on_change=lambda _, item=item: item.toggle())
            input = ui.input(value=item.name).classes('flex-grow')
            input.on('keydown.enter', lambda _, item=item, input=input: item.set_name(input.value))
            ui.button(on_click=lambda _, item=item: todos.remove(item)).props('flat fab-mini icon=delete color=grey')


todos = ToDoList('Shopping', on_change=todo_ui.refresh)
todos.add('Buy milk', done=True)
todos.add('Clean the house')
todos.add('Call mom')

with ui.card().classes('w-80 items-stretch'):
    ui.label().bind_text_from(todos, 'title').classes('text-semibold text-2xl')
    todo_ui()
    add_input = ui.input('New item').classes('mx-12')
    add_input.on('keydown.enter', lambda: (todos.add(add_input.value), add_input.set_value('')))

ui.run()
