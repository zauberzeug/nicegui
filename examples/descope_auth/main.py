#!/usr/bin/env python3
import json

import user

from nicegui import ui


@user.login_page
def login():
    """
    Logs in the user and opens the main page upon successful login.

    This function triggers the login form and listens for the 'success' event.
    When the login form is successfully submitted, it executes the lambda function
    that opens the main page.

    Example usage:
    login()

    """
    user.login_form().on('success', lambda: ui.open('/'))


@user.page('/')
def home():
    """
    Renders the home page of the application.

    This function displays the user's information in JSON format using the `ui.code` method.
    It also provides a logout button that triggers the `user.logout` function when clicked.

    Usage:
        - Call this function to render the home page of the application.

    """
    ui.code(json.dumps(user.about(), indent=2), language='json')
    ui.button('Logout', on_click=user.logout)


@user.page('/async')
async def async_page():
    """
    This is an async page function that demonstrates the usage of NiceGUI library.
    
    When called, it waits for the 'Wait for it...' button to be clicked and then displays a label.
    This function should be used within a NiceGUI application to create an asynchronous page.
    """
    await ui.button('Wait for it...').clicked()
    ui.label('This is an async page')


ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED')
