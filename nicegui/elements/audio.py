import warnings

from ..dependencies import register_component
from ..element import Element

register_component('audio', __file__, 'audio.js')


class Audio(Element):

    def __init__(self, src: str, *,
                 controls: bool = True,
                 autoplay: bool = False,
                 muted: bool = False,
                 loop: bool = False,
                 type: str = '',  # DEPRECATED
                 ) -> None:
        """Audio

        :param src: URL of the audio source
        :param controls: whether to show the audio controls, like play, pause, and volume (default: `True`)
        :param autoplay: whether to start playing the audio automatically (default: `False`)
        :param muted: whether the audio should be initially muted (default: `False`)
        :param loop: whether the audio should loop (default: `False`)

        See `here <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio#events>`_
        for a list of events you can subscribe to using the generic event subscription `on()`.
        """
        super().__init__('audio')
        self._props['src'] = src
        self._props['controls'] = controls
        self._props['autoplay'] = autoplay
        self._props['muted'] = muted
        self._props['loop'] = loop

        if type:
            url = f'https://github.com/zauberzeug/nicegui/pull/624'
            warnings.warn(DeprecationWarning(f'The type parameter for ui.audio is deprecated and ineffective ({url}).'))
