import justpy as jp
from elements import Column, Page

page = Page()
content = Column(page.view)

jp.justpy(lambda: page.view, start_server=False)
ui = jp.app

# bind methods to simplify API -- justpy creates an app which must be found by uvicorn via string "module:attribute"
for field in dir(content):
    if field[0] != '_' and callable(attr := getattr(content, field)):
        setattr(ui, field, attr)
ui.timer = page.timer
