from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from .image import Image

if TYPE_CHECKING:
    from PIL.Image import Image as PIL_Image


class Parallax(Image, component='image.js'):

    def __init__(self, source: str | Path | PIL_Image = '', *, height: float = 500.0, speed: float = 1.0) -> None:
        """Parallax Image

        Displays an image with a parallax effect.
        This element is based on Quasar's `Parallax <https://quasar.dev/vue-components/parallax>`_ component.

        *Added in version 3.9.0.*

        :param source: the source of the image; can be a URL, local file path, a base64 string or a PIL image
        :param height: the height of the parallax image in pixels (default: 500.0)
        :param speed: the speed (0 to 1) of the parallax effect (default: 1.0)
        """
        super().__init__(source=source)
        self._props['height'] = height
        self._props['speed'] = speed
        self._props['tag'] = 'q-parallax'
