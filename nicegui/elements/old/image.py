import justpy as jp

from ..binding import BindableProperty, BindSourceMixin
from .group import Group


class Image(Group, BindSourceMixin):
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
