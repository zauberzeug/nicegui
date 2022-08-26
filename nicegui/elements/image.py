import justpy as jp

from ..binding import BindableProperty, bind_from, bind_to
from .group import Group


class Image(Group):
    source = BindableProperty()

    def __init__(self, source: str = ''):
        """Image

        Displays an image.

        :param source: the source of the image; can be an URL or a base64 string
        """
        view = jp.QImg(src=source, temp=False)
        super().__init__(view)

        self.source = source
        self.bind_source_to(self.view, 'src')

    def set_source(self, source: str):
        self.source = source

    def bind_source_to(self, target_object, target_name, forward=lambda x: x):
        bind_to(self, 'source', target_object, target_name, forward=forward)
        return self

    def bind_source_from(self, target_object, target_name, backward=lambda x: x):
        bind_from(self, 'source', target_object, target_name, backward=backward)
        return self

    def bind_source(self, target_object, target_name, forward=lambda x: x, backward=lambda x: x):
        bind_from(self, 'source', target_object, target_name, backward=backward)
        bind_to(self, 'source', target_object, target_name, forward=forward)
        return self
