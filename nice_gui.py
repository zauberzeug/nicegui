import traceback
import justpy as jp
from icecream import ic
from contextlib import contextmanager


class NiceGui():

    def __init__(self):

        self.context = [jp.WebPage(delete_flag=False)]

        def build():
            return self.context[0]

        jp.justpy(build, start_server=False)

    @property
    def current(self):

        return self.context[-1]

    def label(self, text):

        p = jp.P(text=text, a=self.current, classes='w-48 text-xl p-1 m-2')

    def button(self, text, on_click=None):

        def click(self, _):
            try:
                on_click(self)
            except:
                traceback.print_exc()

        d = jp.Div(text=text, a=self.current, classes='w-48 text-xl m-2 p-1 bg-blue-700 text-white text-center')
        d.on('click', click)

    @contextmanager
    def column(self):
        d = jp.Div(a=self.current, classes='flex flex-wrap')
        self.context.append(d)
        yield
        self.context.pop()


nice_gui = NiceGui()
ui = jp.app

# bind methods to simplify API -- justpy creates an app which must be found by uvicorn via string "module:attribute"
ui.label = nice_gui.label
ui.button = nice_gui.button
ui.column = nice_gui.column 
