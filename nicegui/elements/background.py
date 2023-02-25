from typing import Literal, Optional

from ..dependencies import register_component
from ..element import Element

register_component('background', __file__, 'background.js')


class Background(Element):
    def __init__(
        self,
        color: Optional[str] = None,
        image_src: Optional[str] = None,
        image_size: Optional[Literal['auto', 'contain', 'cover']] = 'auto',
        image_position: Optional[dict[str, str]] = None,
        image_repeat: Optional[
            Literal['repeat', 'repeat-x', 'repeat-y', 'no-repeat']
        ] = None,
        video_src: Optional[str] = None,
    ) -> None:
        """Background Configurator

        Element to configure the background of the application. There are three options:

        1. Color: set a solid color for the app's background.
        2. Image: define an image, and its visualization behavior, for the background of the app.
        3. Set a video (.mp4) to run in a loop and muted, as the background of the app.

        :param color: CSS color to be used in the background
        :param image_src: link to the image to be used in the background
        :param image_size: image size
        :param image_position: image position
        :param image_repeat: image repeat pattern
        :param video_src: video link to be used in the background
        """

        super().__init__('background')

        if color is not None:
            self._props['color'] = color

        if image_src is not None:
            self._props['image'] = {
                'src': image_src,
                'size': image_size,
                'position': image_position,
                'repeat': image_repeat,
            }

        if video_src is not None:
            self._props['video'] = video_src
