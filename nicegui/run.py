import inspect
import sys
import webbrowser
import uvicorn
from .elements.element import Element
from .config import config  # NOTE: before justpy
import justpy as jp

if not config.interactive and config.reload and not inspect.stack()[-2].filename.endswith('spawn.py'):

    if config.show:
        webbrowser.open(f'http://{config.host}:{config.port}/')
    uvicorn.run('nicegui:app', host=config.host, port=config.port, lifespan='on', reload=True)
    sys.exit()

def run(self, *, host='0.0.0.0', port=80, title='NiceGUI', favicon='favicon.ico', reload=True, show=True):

    if config.interactive or reload == False:  # NOTE: if reload == True we already started uvicorn above
        if show:
            webbrowser.open(f'http://{host if host != "0.0.0.0" else "127.0.0.1"}:{port}/')
        Element.wp.title = title
        Element.wp.favicon = favicon
        uvicorn.run(jp.app, host=host, port=port, lifespan='on')
