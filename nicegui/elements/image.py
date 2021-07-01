import justpy as jp
from .element import Element
from .group import Group

class Image(Group):

    def __init__(self,
                 source: str = '',
                 ):
        """Image Element

        Displays an image.

        :param source: the source of the image; can be an url or a base64 string
        """

        view = jp.QImg(src=source)

        super().__init__(view)

    @property
    def source(self):

        return self.view.src

    @source.setter
    def source(self, source: any):

        self.view.src = source

    def set_source(self, source: str):

        self.source = source

    def bind_source_to(self, target, forward=lambda x: x):

        self.source.bind_to(target, forward=forward, nesting=1)
        return self

    def bind_source_from(self, target, backward=lambda x: x):

        self.source.bind_from(target, backward=backward, nesting=1)
        return self

    def bind_source(self, target, forward=lambda x: x, backward=lambda x: x):

        self.source.bind(target, forward=forward, backward=backward, nesting=1)
        return self
