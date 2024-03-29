from nicegui import ui

from . import doc


@doc.demo(ui.monaco)
def main_demo():
    ui.monaco(language="python", theme="vs-dark", value="print('Hello, world!')", minimap=True)
