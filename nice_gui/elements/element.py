import justpy as jp

class Element:

    wp: None
    view_stack = []

    def __init__(self, view: jp.HTMLBaseComponent):

        self.view_stack[-1].add(view)
        view.add_page(self.wp)
        self.view = view
