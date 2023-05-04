#!/usr/bin/env python3
import sqlite3
from pathlib import Path
from typing import Any, Dict

from nicegui import ui

DB_FILE = Path(__file__).parent / 'users.db'
DB_FILE.touch()
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id integer primary key AUTOINCREMENT, name text, age integer)')
conn.commit()


@ui.refreshable
def users_ui() -> None:
    cursor.execute('SELECT * FROM users')
    for row in cursor.fetchall():
        user = {'id': row[0], 'name': row[1], 'age': row[2]}
        with ui.card():
            with ui.row().classes('justify-between w-full'):
                ui.label(user['id'])
                ui.label(user['name'])
                ui.label(user['age'])
            with ui.row():
                ui.button('edit', on_click=lambda _, user=user: open_dialog(user))
                ui.button('delete', on_click=lambda _, user=user: delete(user), color='red')


def create() -> None:
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name.value, age.value))
    conn.commit()
    ui.notify(f'Created new user {name.value}')
    name.value = ''
    age.value = None
    users_ui.refresh()


def update() -> None:
    query = 'UPDATE users SET name=?, age=? WHERE id=?'
    cursor.execute(query, (dialog_name.value, dialog_age.value, dialog_id))
    conn.commit()
    ui.notify(f'Updated user {dialog_name.value}')
    dialog.close()
    users_ui.refresh()


def delete(user: Dict[str, Any]) -> None:
    cursor.execute('DELETE from users WHERE id=?', (user['id'],))
    conn.commit()
    ui.notify(f'Deleted user {user["name"]}')
    users_ui.refresh()


def open_dialog(user: Dict[str, Any]) -> None:
    global dialog_id
    dialog_id = user['id']
    dialog_name.value = user['name']
    dialog_age.value = user['age']
    dialog.open()


name = ui.input(label='Name')
age = ui.number(label='Age', format='%.0f')
ui.button('Add new user', on_click=create)

users_ui()

with ui.dialog() as dialog:
    with ui.card():
        dialog_id = None
        dialog_name = ui.input('Name')
        dialog_age = ui.number('Age', format='%.0f')
        with ui.row():
            ui.button('Save', on_click=update)
            ui.button('Close', on_click=dialog.close).props('outline')

ui.run()
