import inspect
import sys
import webbrowser
import uvicorn
from .config import config  # NOTE: before justpy
import justpy as jp

if config.reload and not inspect.stack()[-2].filename.endswith('spawn.py'):

    if config.show:
        webbrowser.open(f'http://{config.host}:{config.port}/')
    uvicorn.run('nicegui:app', host=config.host, port=config.port, lifespan='on', reload=True)
    sys.exit()

def run(self, *, host='0.0.0.0', port=80, title='NiceGUI', favicon='favicon.png', reload=True, show=True):

    if reload == False:  # NOTE: in case reload == True we already started uvicorn above
        if show:
            webbrowser.open(f'http://{host}:{port}/')
        uvicorn.run(jp.app, host=host, port=port, lifespan='on')
