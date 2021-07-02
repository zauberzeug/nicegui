from .element import Element

class Group(Element):

    def __enter__(self):

        self.view_stack.append(self.view)
        return self

    def __exit__(self, *_):

        self.view_stack.pop()
