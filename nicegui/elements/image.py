import base64
import io
import time
from pathlib import Path
from typing import Union

from .. import optional_features
from ..logging import log
from .mixins.source_element import SourceElement

try:
    from PIL.Image import Image as PIL_Image
    optional_features.register('pillow')
except ImportError:
    pass


class Image(SourceElement, component='image.js'):
    PIL_CONVERT_FORMAT = 'PNG'

    def __init__(self, source: Union[str, Path, 'PIL_Image'] = '') -> None:
        """Image

        Displays an image.
        This element is based on Quasar's `QImg <https://quasar.dev/vue-components/img>`_ component.

        :param source: the source of the image; can be a URL, local file path, a base64 string or a PIL image
        """
        super().__init__(source=source)

    def set_source(self, source: Union[str, Path, 'PIL_Image']) -> None:
        return super().set_source(source)

    def _set_props(self, source: Union[str, Path, 'PIL_Image']) -> None:
        if optional_features.has('pillow') and isinstance(source, PIL_Image):
            source = pil_to_base64(source, self.PIL_CONVERT_FORMAT)
        super()._set_props(source)

    def force_reload(self) -> None:
        """Force the image to reload from the source."""
        if self._props['src'].startswith('data:'):
            log.warning('ui.image: force_reload() only works with network sources (not base64)')
            return
        self._props['t'] = time.time()
        self.update()


def pil_to_base64(pil_image: 'PIL_Image', image_format: str) -> str:
    """Convert a PIL image to a base64 string which can be used as image source.

    :param pil_image: the PIL image
    :param image_format: the image format
    :return: the base64 string
    """
    buffer = io.BytesIO()
    pil_image.save(buffer, image_format)
    base64_encoded = base64.b64encode(buffer.getvalue())
    base64_string = base64_encoded.decode('utf-8')
    return f'data:image/{image_format.lower()};base64,{base64_string}'
