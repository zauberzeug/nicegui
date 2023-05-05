#!/usr/bin/env python3
import c
import example_pages
import home_page
import theme

from nicegui import app, ui


# here we use our custom page decorator directly and just put the content creation into a separate function
@ui.page('/')
def index_page() -> None:
    with theme.frame('Homepage'):
        home_page.content()


# this call shows that you can also move the whole page creation into a separate file
example_pages.create()

app.include_router(c.router)

ui.run(title='Modularization Example')
