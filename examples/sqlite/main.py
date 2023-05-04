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
                ui.button('edit', on_click=lambda _, user=user: edit(user))
                ui.button('delete', on_click=lambda _, user=user: delete(user), color='red')


def add() -> None:
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name.value, age.value))
    conn.commit()
    ui.notify(f'Added new user {name.value}', type='positive')
    name.value = ''
    age.value = None
    users_ui.refresh()


def save() -> None:
    query = 'UPDATE users SET name=?, age=? WHERE id=?'
    cursor.execute(query, (dialog_name.value, dialog_age.value, dialog_id))
    conn.commit()
    ui.notify(f'Updated user {dialog_name.value}', type='positive')
    dialog.close()
    users_ui.refresh()


def edit(user: Dict[str, Any]) -> None:
    global dialog_id
    dialog_id = user['id']
    dialog_name.value = user['name']
    dialog_age.value = user['age']
    dialog.open()


def delete(user: Dict[str, Any]) -> None:
    cursor.execute('DELETE from users WHERE id=?', (user['id'],))
    conn.commit()
    users_ui.refresh()


name = ui.input(label='Name')
age = ui.number(label='Age', format='%.0f')
ui.button('Add new user', on_click=add)

users_ui()

with ui.dialog() as dialog:
    with ui.card():
        ui.label('Edit User').classes('font-xl font-bold')
        dialog_id = None
        dialog_name = ui.input('Name')
        dialog_age = ui.number('Age', format='%.0f')
        with ui.row():
            ui.button('Save', on_click=save)
            ui.button('Close', on_click=dialog.close).props('outline')

ui.run()
