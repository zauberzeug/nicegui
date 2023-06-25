#!/usr/bin/env python3
from datetime import datetime
from typing import List, Tuple
from uuid import uuid4
from nicegui import ui
import sqlite3
import recommend as r


def get_cocktails(cocktail_ids):
    # Create a connection to your database.
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    id_list = ','.join(map(str, cocktail_ids))

    # Execute the query.
    cursor.execute(f'SELECT * FROM cocktail WHERE id IN ({id_list})')
    data = cursor.fetchall()

    # Close the connection.
    cursor.close()
    conn.close()

    # Return the fetched data.
    return data


def get_carousel_img(cocktail_ids):
    # Create a connection to your database.
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    id_list = ','.join(map(str, cocktail_ids))

    # Execute the query.
    cursor.execute(
        f'select DISTINCT liquor.img_src from liquor, cocktail, cocktail_liquor where cocktail_liquor.liquor_id = liquor.id and cocktail_liquor.cocktail_id = cocktail.id and cocktail_id IN ({id_list})')
    data = cursor.fetchall()

    # Close the connection.
    cursor.close()
    conn.close()

    # Return the fetched data.
    return data


def get_all_cocktails():
    # Create a connection to your database.
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Execute the query.
    cursor.execute('SELECT * FROM cocktail')
    data = cursor.fetchall()

    # Close the connection.
    cursor.close()
    conn.close()

    # Return the fetched data.
    return data


def action(cocktail_id, rating):
    # Create a connection to your database.
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Check if a row already exists for this user and cocktail.
    cursor.execute('SELECT * FROM user_cocktail WHERE user_id = ? AND cocktail_id = ?', (user_id, cocktail_id))
    row = cursor.fetchone()

    if row is None:
        cursor.execute('SELECT * FROM user_cocktail ORDER BY id DESC LIMIT 1')
        last_id = cursor.fetchone()
        print(last_id[0])
        # If no row exists, insert a new one.
        cursor.execute('INSERT INTO user_cocktail (id, user_id, cocktail_id, rating) VALUES (?, ?, ?, ?)',
                       (last_id[0] + 1, user_id, cocktail_id, rating))
    else:
        # If a row exists, update it.
        cursor.execute('UPDATE user_cocktail SET rating = ? WHERE user_id = ? AND cocktail_id = ?',
                       (rating, user_id, cocktail_id))

    # Commit changes and close the connection.
    conn.commit()
    cursor.close()
    conn.close()

    if rating == 1:
        print(f"Cocktail {cocktail_id} disliked")
    if rating == 5:
        print(f"Cocktail {cocktail_id} liked")


messages: List[Tuple[str, str, str, str]] = []

user_id = 1
recommended = r.m(user_id)
cocktails = get_cocktails(recommended)
liquor_img = get_carousel_img(recommended)
all_cocktails = get_all_cocktails()


tabs = {}


def switch_tab(value):
    tabs['panels'].value = value


tab_bar = ui.tabs()

with ui.tab_panels(tab_bar, value=1).classes('w-full') as panels:
    tabs['panels'] = panels

    for i, img in enumerate(liquor_img):
        with ui.tab_panel(i):
            with ui.card().classes('m-4 p-4 shadow-lg w-128 h-64 relative'):
                with ui.card().classes('w-full h-full absolute'):
                    ui.image(img[0]).classes('w-full h-full')
                    ui.button(on_click=lambda i=i: switch_tab(max(i - 1, 0)), icon='arrow_back').classes(
                        'absolute top-1/2 left-2')  # max(i-1, 0) to prevent going to negative indices
                    ui.button(on_click=lambda i=i: switch_tab(min(i + 1, len(liquor_img) - 1)),
                              icon='arrow_forward').classes(
                        'absolute top-1/2 right-2')  # min(i+1, len(liquor_img)-1) to prevent going beyond the last index

with ui.row():
    ui.label("For you").classes('mt-2 text-2xl font-bold')
    for i, (cocktail_id, cocktail_name, cocktail_desc, cocktail_img) in enumerate(cocktails):
        with ui.card().classes('m-4 p-4 shadow-lg relative').style('width: 300px'):
            ui.image(cocktail_img).classes('w-full h-full')
            ui.label(cocktail_name).classes('mt-2')
            ui.label(cocktail_desc).classes('mt-2')
            with ui.row().classes('justify-between mt-2'):
                ui.button(on_click=lambda i=i: action(cocktail_id, 5), icon='thumb_up').classes('fab')
                ui.button(on_click=lambda i=i: action(cocktail_id, 1), icon='thumb_down').classes('fab')

with ui.row():
    ui.label("Our Menu").classes('mt-2 text-2xl font-bold')
    for i, (cocktail_id, cocktail_name, cocktail_desc, cocktail_img) in enumerate(all_cocktails):
        with ui.card().classes('m-4 p-4 shadow-lg relative').style('width: 300px'):
            ui.image(cocktail_img).classes('w-full h-full')
            ui.label(cocktail_name).classes('mt-2')
            ui.label(cocktail_desc).classes('mt-2')
            with ui.row().classes('justify-between mt-2'):
                ui.button(on_click=lambda i=i: action(cocktail_id, 5), icon='thumb_up').classes('fab')
                ui.button(on_click=lambda i=i: action(cocktail_id, 1), icon='thumb_down').classes('fab')


with ui.footer(value=False) as footer:
    ui.label('Footer')

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

ui.run()
