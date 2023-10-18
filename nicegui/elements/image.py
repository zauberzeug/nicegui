from pathlib import Path
from typing import Union

from .mixins.source_element import SourceElement


class Image(SourceElement, component='image.js'):

    def __init__(self, source: Union[str, Path] = '') -> None:
        """Image

        Displays an image.
        This element is based on Quasar's `QImg <https://quasar.dev/vue-components/img>`_ component.

        :param source: the source of the image; can be a URL, local file path or a base64 string
        """
        super().__init__(source=source)
