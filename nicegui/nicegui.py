#!/usr/bin/env python3
import justpy as jp
import uvicorn
import sys
import inspect
import webbrowser
import docutils.core
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from .ui import Ui
from .timer import Timer
from .elements.element import Element
from .binding import Binding

# start uvicorn with auto-reload; afterwards the auto-reloaded process should not start uvicorn again
if not inspect.stack()[-2].filename.endswith('spawn.py'):
    webbrowser.open('http://localhost/')
    uvicorn.run('nicegui:app', host='0.0.0.0', port=80, lifespan='on', reload=True)
    sys.exit()

wp = jp.QuasarPage(delete_flag=False, title='NiceGUI', favicon='favicon.png')
wp.css = HtmlFormatter().get_style_defs('.codehilite')
wp.head_html = '<script>confirm = () => true;</script>'  # avoid confirmation dialog for reload
wp.head_html += docutils.core.publish_parts('', writer_name='html')['stylesheet']


main = jp.Div(a=wp, classes='q-ma-md column items-start', style='row-gap: 1em')
main.add_page(wp)
jp.justpy(lambda: wp, start_server=False)

@jp.app.on_event('startup')
def startup():
    [jp.run_task(t) for t in Timer.tasks]
    jp.run_task(Binding.loop())

Element.wp = wp
Element.view_stack = [main]

app = jp.app
ui = Ui()
