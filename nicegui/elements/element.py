import justpy as jp

class Element:

    wp: None
    view_stack = []

    def __init__(self, view: jp.HTMLBaseComponent):

        self.view_stack[-1].add(view)
        view.add_page(self.wp)
        self.view = view

    def set_classes(self, classes: str):

        self.view.classes = classes
        return self

    def add_classes(self, classes: str):

        self.view.classes += ' ' + classes
        return self

    def set_style(self, style: str):

        self.view.style = style
        return self

    def add_style(self, style: str):

        self.view.style += ' ' + style
        return self
