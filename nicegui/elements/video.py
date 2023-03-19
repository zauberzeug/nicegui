from ..dependencies import register_component
from ..element import Element

register_component('video', __file__, 'video.js')


class Video(Element):

    def __init__(self, src: str, *,
                 type: str = 'video/mp4',
                 controls: bool = True,
                 autoplay: bool = False,
                 muted: bool = False,
                 loop: bool = False) -> None:
        """Video

        :param src: URL of the video source
        :param type: MIME-type of the resource (default: 'video/mp4')
        :param controls: whether to show the video controls, like play, pause, and volume (default: `True`)
        :param autoplay: whether to start playing the video automatically (default: `False`)
        :param muted: whether the video should be initially muted (default: `False`)
        :param loop: whether the video should loop (default: `False`)

        See `here <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video#events>`_
        for a list of events you can subscribe to using the generic event subscription `on()`.
        """
        super().__init__('video')
        self._props['src'] = src
        self._props['type'] = type
        self._props['controls'] = controls
        self._props['autoplay'] = autoplay
        self._props['muted'] = muted
        self._props['loop'] = loop
