from .mixins.source_element import SourceElement


class Image(SourceElement):

    def __init__(self, source: str = '') -> None:
        """Image

        Displays an image.

        :param source: the source of the image; can be a URL or a base64 string
        """
        super().__init__(tag='q-img', source=source)
