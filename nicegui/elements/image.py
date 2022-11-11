from ..binding import BindSourceMixin
from ..element import Element


class Image(Element, BindSourceMixin):

    def __init__(self, source: str = '') -> None:
        """Image

        Displays an image.

        :param source: the source of the image; can be a URL or a base64 string
        """
        super().__init__('q-img')
        self.source = source
        self._props['src'] = source

    def on_source_change(self, source: str) -> None:
        self._props['src'] = source
        self.update()
