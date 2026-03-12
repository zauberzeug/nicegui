from pathlib import Path

from ..defaults import DEFAULT_PROP, resolve_defaults
from .mixins.source_element import SourceElement


class Video(SourceElement, component='video.js'):
    SOURCE_IS_MEDIA_FILE = True

    @resolve_defaults
    def __init__(self, src: str | Path, *,
                 controls: bool = DEFAULT_PROP | True,
                 autoplay: bool = DEFAULT_PROP | False,
                 muted: bool = DEFAULT_PROP | False,
                 loop: bool = DEFAULT_PROP | False,
                 ) -> None:
        """Video

        Displays a video.

        :param src: URL or local file path of the video source
        :param controls: whether to show the video controls, like play, pause, and volume (default: `True`)
        :param autoplay: whether to start playing the video automatically (default: `False`)
        :param muted: whether the video should be initially muted (default: `False`)
        :param loop: whether the video should loop (default: `False`)

        See `here <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video#events>`_
        for a list of events you can subscribe to using the generic event subscription `on()`.
        """
        super().__init__(source=src)
        self._props.set_bool('controls', controls)
        self._props.set_bool('autoplay', autoplay)
        self._props.set_bool('muted', muted)
        self._props.set_bool('loop', loop)

    def set_source(self, source: str | Path) -> None:
        return super().set_source(source)

    def seek(self, seconds: float) -> None:
        """Seek to a specific position in the video.

        :param seconds: the position in seconds
        """
        self.run_method('seek', seconds)

    def play(self) -> None:
        """Play video."""
        self.run_method('play')

    def pause(self) -> None:
        """Pause video."""
        self.run_method('pause')
