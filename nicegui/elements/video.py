import warnings
from pathlib import Path
from typing import Union

from .. import globals
from ..element import Element


class Video(Element, component='video.js'):

    def __init__(self, src: Union[str, Path], *,
                 controls: bool = True,
                 autoplay: bool = False,
                 muted: bool = False,
                 loop: bool = False,
                 type: str = '',  # DEPRECATED
                 ) -> None:
        """Video

        :param src: URL or local file path of the video source
        :param controls: whether to show the video controls, like play, pause, and volume (default: `True`)
        :param autoplay: whether to start playing the video automatically (default: `False`)
        :param muted: whether the video should be initially muted (default: `False`)
        :param loop: whether the video should loop (default: `False`)

        See `here <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video#events>`_
        for a list of events you can subscribe to using the generic event subscription `on()`.
        """
        super().__init__()
        if Path(src).is_file():
            src = globals.app.add_media_file(local_file=src)
        self._props['src'] = src
        self._props['controls'] = controls
        self._props['autoplay'] = autoplay
        self._props['muted'] = muted
        self._props['loop'] = loop

        if type:
            url = f'https://github.com/zauberzeug/nicegui/pull/624'
            warnings.warn(DeprecationWarning(f'The type parameter for ui.video is deprecated and ineffective ({url}).'))

    def seek(self, seconds: float) -> None:
        """Seek to a specific position in the video.

        :param seconds: the position in seconds
        """
        self.run_method('seek', seconds)
