import traceback
import justpy as jp
from icecream import ic

pages = []


def app():

    pages.append(jp.WebPage(delete_flag=False))

    def build():
        return pages[0]

    jp.justpy(build, start_server=False)
    return jp.app


class Widget:

    def __init__(self):
        pass


class Label(Widget):

    def __init__(self, text):

        super().__init__()
        p = jp.P(text=text, a=pages[0], classes='w-48 text-xl p-1 m-2')


class Button(Widget):

    def __init__(self, text, on_click=None):

        super().__init__()

        def click(self, _):
            try:
                on_click(self)
            except:
                traceback.print_exc()

        d = jp.Div(text=text, a=pages[0], classes='w-48 text-xl m-2 p-1 bg-blue-700 text-white text-center')
        d.on('click', click)
