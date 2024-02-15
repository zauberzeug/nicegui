#!/usr/bin/env python3
from typing import List

import models
from tortoise import Tortoise

from nicegui import app, ui


async def init_db() -> None:
    """
    Initialize the database connection and generate the schemas.

    This function initializes the Tortoise ORM database connection using the specified
    SQLite database URL and the models defined in the 'models' module. It then generates
    the database schemas based on the defined models.

    Parameters:
        None

    Returns:
        None

    Example usage:
        await init_db()
    """
    await Tortoise.init(db_url='sqlite://db.sqlite3', modules={'models': ['models']})
    await Tortoise.generate_schemas()


async def close_db() -> None:
    """
    Closes the connections to the SQLite database.

    This function is used to gracefully close the connections to the SQLite database
    when it is no longer needed. It ensures that all pending transactions are committed
    and the connections are properly closed.

    Returns:
        None

    Raises:
        None
    """
    await Tortoise.close_connections()

app.on_startup(init_db)
app.on_shutdown(close_db)


@ui.refreshable
async def list_of_users() -> None:
    """
    Retrieves a list of users from the database and displays them in a UI card format.
    Allows editing the user's name and age, as well as deleting a user.

    Usage:
    - Call this function to display the list of users in the UI.
    - Edit the user's name or age by modifying the corresponding input fields.
    - Changes are automatically saved to the database when the input fields lose focus.
    - Click the delete button to remove a user from the database.

    Note:
    - The UI is refreshed after any changes to ensure the latest data is displayed.
    """
    async def delete(user: models.User) -> None:
        await user.delete()
        list_of_users.refresh()

    users: List[models.User] = await models.User.all()
    for user in reversed(users):
        with ui.card():
            with ui.row().classes('items-center'):
                ui.input('Name', on_change=user.save) \
                    .bind_value(user, 'name').on('blur', list_of_users.refresh)
                ui.number('Age', on_change=user.save, format='%.0f') \
                    .bind_value(user, 'age').on('blur', list_of_users.refresh).classes('w-20')
                ui.button(icon='delete', on_click=lambda u=user: delete(u)).props('flat')


@ui.page('/')
async def index():
    """
    This function represents the main entry point of the program.
    It is responsible for creating a user in the database based on the provided name and age values.
    The function also refreshes the list of users after creating a new user.

    Usage:
    - Call this function to create a user in the database.
    - Provide the name and age values as input.
    - The function will create a new user with the provided name and age.
    - The list of users will be refreshed to reflect the changes.

    Example:
    ```
    await index()
    ```

    Parameters:
    - None

    Returns:
    - None
    """
    async def create() -> None:
        await models.User.create(name=name.value, age=age.value or 0)
        name.value = ''
        age.value = None
        list_of_users.refresh()

    with ui.column().classes('mx-auto'):
        with ui.row().classes('w-full items-center px-4'):
            name = ui.input(label='Name')
            age = ui.number(label='Age', format='%.0f').classes('w-20')
            ui.button(on_click=create, icon='add').props('flat').classes('ml-auto')
        await list_of_users()

ui.run()
