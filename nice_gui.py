import justpy as jp
from elements import Page

main = Page()
ui = jp.app

# bind methods to simplify API -- justpy creates an app which must be found by uvicorn via string "module:attribute"
for field in dir(main):
    if field[0] != '_' and callable(attr := getattr(main, field)):
        setattr(ui, field, attr)
