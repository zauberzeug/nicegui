#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List

from nicegui import ui


@dataclass
class TodoItem:
    name: str
    done: bool = False


items: List[TodoItem] = [
    TodoItem('Buy milk', done=True),
    TodoItem('Clean the house'),
    TodoItem('Call mom'),
]


def add(name: str) -> None:
    items.append(TodoItem(name))
    add_input.value = None
    render_list.refresh()


def remove(item: TodoItem) -> None:
    items.remove(item)
    render_list.refresh()


def toggle(item: TodoItem) -> None:
    item.done = not item.done
    render_list.refresh()


def rename(item: TodoItem, name: str) -> None:
    item.name = name
    render_list.refresh()


with ui.card().classes('w-80 items-stretch'):
    ui.label('Todo list').classes('text-semibold text-2xl')
    add_input = ui.input('New item')
    add_input.on('keydown.enter', lambda: add(add_input.value))

    @ui.refreshable
    def render_list():
        if not items:
            ui.label('List is empty.')
            return
        ui.linear_progress(sum(item.done for item in items) / len(items), show_value=False)
        with ui.row():
            ui.label(f'Completed: {sum(item.done for item in items)}')
            ui.label(f'Remaining: {sum(not item.done for item in items)}')
        for item in items:
            with ui.row().classes('items-center'):
                ui.checkbox(value=item.done, on_change=lambda _, item=item: toggle(item))
                input = ui.input(value=item.name).classes('flex-grow')
                input.on('keydown.enter', lambda _, item=item, input=input: rename(item, input.value))
                ui.button(on_click=lambda _, item=item: remove(item)).props('flat fab-mini icon=delete color=grey')

    render_list()

ui.run()
