import tempfile
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
            self._source_for_cleanup = pil_to_tempfile(source, self.PIL_CONVERT_FORMAT)
        super()._set_props(self._source_for_cleanup)

    def force_reload(self) -> None:
        """Force the image to reload from the source."""
        if self._props['src'].startswith('data:'):
            log.warning('ui.image: force_reload() only works with network sources (not base64)')
            return
        self._props['t'] = time.time()


def pil_to_tempfile(pil_image: 'PIL_Image', image_format: str) -> Path:
    """Save a PIL image to a temporary file.

    :param pil_image: the PIL image
    :param image_format: the image format
    :return: the path to the temporary file
    """
    suffix = f'.{image_format.lower()}'
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        pil_image.save(temp_file, image_format)
        return Path(temp_file.name)
