from pathlib import Path
from typing import Union

from .mixins.source_element import SourceElement


class Audio(SourceElement, component='audio.js'):
    SOURCE_IS_MEDIA_FILE = True

    def __init__(self, src: Union[str, Path], *,
                 controls: bool = True,
                 autoplay: bool = False,
                 muted: bool = False,
                 loop: bool = False,
                 ) -> None:
        """Audio

        Displays an audio player.

        :param src: URL or local file path of the audio source
        :param controls: whether to show the audio controls, like play, pause, and volume (default: `True`)
        :param autoplay: whether to start playing the audio automatically (default: `False`)
        :param muted: whether the audio should be initially muted (default: `False`)
        :param loop: whether the audio should loop (default: `False`)

        See `here <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio#events>`_
        for a list of events you can subscribe to using the generic event subscription `on()`.
        """
        super().__init__(source=src)
        self._props['controls'] = controls
        self._props['autoplay'] = autoplay
        self._props['muted'] = muted
        self._props['loop'] = loop

    def set_source(self, source: Union[str, Path]) -> None:
        return super().set_source(source)

    def seek(self, seconds: float) -> None:
        """Seek to a specific position in the audio.

        :param seconds: the position in seconds
        """
        self.run_method('seek', seconds)

    def play(self) -> None:
        """Play audio."""
        self.run_method('play')

    def pause(self) -> None:
        """Pause audio."""
        self.run_method('pause')
