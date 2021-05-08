import uvicorn
import justpy as jp
from elements import Column, Page
import icecream
import traceback

icecream.install()

page = Page()
ic()
ui = Column(page.view)
jp.justpy(lambda: page.view, start_server=False)

app = jp.app


def _run():
    ic()
    uvicorn.run("main:app", host='0.0.0.0', port=80, lifespan='on', reload=True)

app.run = _run
