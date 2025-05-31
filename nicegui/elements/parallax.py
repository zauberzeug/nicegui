from pathlib import Path
from typing import Union

from .. import optional_features
from .image import Image

try:
    from PIL.Image import Image as PIL_Image
    optional_features.register('pillow')
except ImportError:
    pass


class Parallax(Image, component='image.js'):
    def __init__(self, source: Union[str, Path, 'PIL_Image'] = '', *,
                 height: int = 500,
                 speed: float = 1.0) -> None:
        """Parallax Image

        Displays an image with a parallax effect.
        This element is based on Quasar's `Parallax <https://quasar.dev/vue-components/parallax>`_ component.

        :param source: the source of the image; can be a URL, local file path, a base64 string or a PIL image
        :param height: the height of the parallax image in pixels (default: 500)
        :param speed: the speed (0 to 1) of the parallax effect (default: 1.0)
        """
        super().__init__(source=source)
        self._props['height'] = height
        self._props['speed'] = speed
        self._props['is_parallax'] = True
