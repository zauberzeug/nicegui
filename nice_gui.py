import uvicorn
import justpy as jp
from elements import Column, Page
import icecream
import traceback
from contextlib import contextmanager
import sys

icecream.install()

@contextmanager
def NiceGui():
    # mod = sys._getframe(2).f_globals["__name__"]
    # ic(mod)
    # if "main" == mod:
    #     return
    page = Page()
    yield Column(page.view)
    jp.justpy(lambda: page.view, start_server=False)

app = jp.app


def _run():
    uvicorn.run("main:app", host='0.0.0.0', port=80, lifespan='on', reload=True)

app.run = _run
