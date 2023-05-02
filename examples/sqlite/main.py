#!/usr/bin/env python3

import sqlite3
from pathlib import Path
from typing import Dict

from nicegui import ui

# initialize sqlite file
DB_FILE = Path(__file__).parent / "db/people.db"
DB_FILE.touch()

conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (id integer primary key AUTOINCREMENT, name text, age integer)"
)
conn.commit


def all_users():
    cursor.execute("SELECT * FROM users")
    res = cursor.fetchall()
    result = [
        {
            col[0]: row[i]
            for i, col in enumerate(cursor.description)
        }
        for row in res
    ]
    return result


@ui.refreshable
def users_ui():
    users = all_users()
    for x in users:
        with ui.card():
            with ui.column():
                with ui.row().classes("justify-between w-full") as carddata:
                    ui.label(x["id"])
                    ui.label(x["name"])
                    ui.label(x["age"])
                with ui.row():
                    ui.button("edit").on(
                        "click", lambda e, carddata=carddata: editdata(carddata)
                    )
                    ui.button("delete").on(
                        "click", lambda e, carddata=carddata: deletedata(carddata)
                    ).classes("bg-red")


def add_newdata():
    """Callback when a new user button is clicked"""
    try:
        cursor.execute(
            "INSERT INTO users (name, age) VALUES (?, ?)", (name.value, age.value)
        )
        conn.commit()
        ui.notify(f"success add new user {name.value}", color="blue")
        name.value = ""
        age.value = ""

        users_ui.refresh()
    except Exception as e:
        ui.notify(f"failed to add new user {name.value}: {e}", color="red")


def save_edit():
    """Callback when user data is saved in edit dialog"""
    try:
        query = "UPDATE users SET name=?, age=? WHERE id=?"
        cursor.execute(query, (edit_name.value, edit_age.value, get_id.text))
        conn.commit()
        ui.notify("success edit user", color="green")
        editdialog.close()

        users_ui.refresh()
    except Exception as e:
        ui.notify(f"failed to edit user, {e}", color="red")


def editdata(data):
    """Callback when user edit button is clicked"""
    get_id.text = data.default_slot.children[0].text
    name.value = data.default_slot.children[1].text
    age.value = data.default_slot.children[2].text

    editdialog.open()
    ui.update()


def deletedata(data):
    """Callback when user delete button is clicked"""
    get_id.text = data.default_slot.children[0].text

    try:
        query = "DELETE from users WHERE id=?"
        cursor.execute(query, (get_id.text,))
        conn.commit()

        users_ui.refresh()
    except Exception as e:
        ui.notify(f"failed to delete user, {e}", color="red")


##########################
# main page UI starts here
##########################
name = ui.input(label="username").classes("w-full")
age = ui.number(label="your age").classes("w-full")

get_id = ui.label()

list_alldata = ui.column()

with ui.dialog() as editdialog:
    with ui.card():
        ui.label("Edit Data").classes("font-xl font-weight")
        edit_name = ui.input().bind_value_from(name, "value")
        edit_age = ui.input().bind_value_from(age, "value")

        with ui.row().classes("justify-between"):
            ui.button("save", on_click=save_edit)
            ui.button("close", on_click=editdialog.close).classes("bg-red")

ui.button("add new person", on_click=add_newdata)
users_ui()

# run GUI main
ui.run()
