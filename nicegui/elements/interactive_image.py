from __future__ import annotations

import time
from pathlib import Path
from typing import List, Optional, Tuple, Union, cast

from typing_extensions import Self

from .. import optional_features
from ..events import GenericEventArguments, Handler, MouseEventArguments, handle_event
from ..logging import log
from .image import pil_to_base64
from .mixins.content_element import ContentElement
from .mixins.source_element import SourceElement

try:
    from PIL.Image import Image as PIL_Image
    optional_features.register('pillow')
except ImportError:
    pass


class InteractiveImage(SourceElement, ContentElement, component='interactive_image.js'):
    CONTENT_PROP = 'content'
    PIL_CONVERT_FORMAT = 'PNG'

    def __init__(self,
                 source: Union[str, Path, 'PIL_Image'] = '', *,  # noqa: UP037
                 content: str = '',
                 size: Optional[Tuple[float, float]] = None,
                 on_mouse: Optional[Handler[MouseEventArguments]] = None,
                 events: List[str] = ['click'],  # noqa: B006
                 cross: Union[bool, str] = False,
                 ) -> None:
        """Interactive Image

        Create an image with an SVG overlay that handles mouse events and yields image coordinates.
        It is also the best choice for non-flickering image updates.
        If the source URL changes faster than images can be loaded by the browser, some images are simply skipped.
        Thereby repeatedly updating the image source will automatically adapt to the available bandwidth.
        See `OpenCV Webcam <https://github.com/zauberzeug/nicegui/tree/main/examples/opencv_webcam/main.py>`_ for an example.

        The mouse event handler is called with mouse event arguments containing

        - `type` (the name of the JavaScript event),
        - `image_x` and `image_y` (image coordinates in pixels),
        - `button` and `buttons` (mouse button numbers from the JavaScript event), as well as
        - `alt`, `ctrl`, `meta`, and `shift` (modifier keys from the JavaScript event).

        You can also pass a tuple of width and height instead of an image source.
        This will create an empty image with the given size.

        :param source: the source of the image; can be an URL, local file path, a base64 string or just an image size
        :param content: SVG content which should be overlaid; viewport has the same dimensions as the image
        :param size: size of the image (width, height) in pixels; only used if `source` is not set
        :param on_mouse: callback for mouse events (contains image coordinates `image_x` and `image_y` in pixels)
        :param events: list of JavaScript events to subscribe to (default: `['click']`)
        :param cross: whether to show crosshairs or a color string (default: `False`)
        """
        super().__init__(source=source, content=content)
        self._props['events'] = events[:]
        self._props['cross'] = cross
        self._props['size'] = size

        if on_mouse:
            self.on_mouse(on_mouse)

    def set_source(self, source: Union[str, Path, 'PIL_Image']) -> None:  # noqa: UP037
        return super().set_source(source)

    def on_mouse(self, on_mouse: Handler[MouseEventArguments]) -> Self:
        """Add a callback to be invoked when a mouse event occurs."""
        def handle_mouse(e: GenericEventArguments) -> None:
            args = cast(dict, e.args)
            arguments = MouseEventArguments(
                sender=self,
                client=self.client,
                type=args.get('mouse_event_type', ''),
                image_x=args.get('image_x', 0.0),
                image_y=args.get('image_y', 0.0),
                button=args.get('button', 0),
                buttons=args.get('buttons', 0),
                alt=args.get('altKey', False),
                ctrl=args.get('ctrlKey', False),
                meta=args.get('metaKey', False),
                shift=args.get('shiftKey', False),
            )
            handle_event(on_mouse, arguments)
        self.on('mouse', handle_mouse)
        return self

    def _set_props(self, source: Union[str, Path, 'PIL_Image']) -> None:  # noqa: UP037
        if optional_features.has('pillow') and isinstance(source, PIL_Image):
            source = pil_to_base64(source, self.PIL_CONVERT_FORMAT)
        super()._set_props(source)

    def force_reload(self) -> None:
        """Force the image to reload from the source."""
        if self._props['src'].startswith('data:'):
            log.warning('ui.interactive_image: force_reload() only works with network sources (not base64)')
            return
        self._props['t'] = time.time()
        self.update()
