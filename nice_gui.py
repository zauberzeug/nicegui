import traceback
import justpy as jp
from icecream import ic


class NiceGui():

    def __init__(self):
        self.index = jp.WebPage(delete_flag=False)

        def build():
            return self.index

        jp.justpy(build, start_server=False)

    def label(self, text):

        p = jp.P(text=text, a=self.index, classes='w-48 text-xl p-1 m-2')

    def button(self, text, on_click=None):

        def click(self, _):
            try:
                on_click(self)
            except:
                traceback.print_exc()

        d = jp.Div(text=text, a=self.index, classes='w-48 text-xl m-2 p-1 bg-blue-700 text-white text-center')
        d.on('click', click)


nice_gui = NiceGui()
ui = jp.app

# bind methods to simplify API -- justpy creates an app which must be found by uvicorn via string "module:attribute"
ui.label = nice_gui.label
ui.button = nice_gui.button
