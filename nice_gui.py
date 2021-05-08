import uvicorn
import justpy as jp
from elements import Column, Page
import icecream
import traceback
from contextlib import contextmanager


icecream.install()

@contextmanager
def NiceGui():
    page = Page()
    jp.justpy(lambda: page.view, start_server=False)
    yield Column(page.view)

app = jp.app


def _run():
    uvicorn.run("main:app", host='0.0.0.0', port=80, lifespan='on', reload=True)

app.run = _run
