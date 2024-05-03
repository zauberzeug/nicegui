#!/usr/bin/env python3
import api_router_example
import class_example
import function_example
import home_page
import theme

from nicegui import app, ui


# Example 1: use a custom page decorator directly and putting the content creation into a separate function
@ui.page('/')
def index_page() -> None:
    with theme.frame('Homepage'):
        home_page.content()


# Example 2: use a function to move the whole page creation into a separate file
function_example.create()

# Example 3: use a class to move the whole page creation into a separate file
class_example.ClassExample()

# Example 4: use APIRouter as described in https://nicegui.io/documentation/page#modularize_with_apirouter
app.include_router(api_router_example.router)

ui.run(title='Modularization Example')
