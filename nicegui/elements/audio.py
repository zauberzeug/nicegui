from pathlib import Path
from typing import Union

from .mixins.source_element import SourceElement


class Audio(SourceElement, component='audio.js'):
    """A class representing an audio player element.

    This class inherits from the `SourceElement` class and provides functionality to display an audio player.

    Args:
    
        - src (Union[str, Path]): The URL or local file path of the audio source.
        - controls (bool, optional): Whether to show the audio controls, like play, pause, and volume. Defaults to True.
        - autoplay (bool, optional): Whether to start playing the audio automatically. Defaults to False.
        - muted (bool, optional): Whether the audio should be initially muted. Defaults to False.
        - loop (bool, optional): Whether the audio should loop. Defaults to False.

    Attributes:
        - SOURCE_IS_MEDIA_FILE (bool): A class attribute indicating that the source is a media file.

    Methods:
        - seek(seconds: float) -> None: Seeks to a specific position in the audio.
        - play() -> None: Plays the audio.
        - pause() -> None: Pauses the audio.

    Examples:
        Create an audio player with controls and autoplay:

        ```python
        audio = Audio("https://example.com/audio.mp3", controls=True, autoplay=True)
        ```

        Seek to a specific position in the audio:

        ```python
        audio.seek(30.5)
        ```

        Play the audio:

        ```python
        audio.play()
        ```

        Pause the audio:

        ```python
        audio.pause()
        ```

    See Also:
        - [HTML Audio Element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio)
        - [HTML Audio Events](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio#events)
    """
    SOURCE_IS_MEDIA_FILE = True

    def __init__(self, src: Union[str, Path], *,
                 controls: bool = True,
                 autoplay: bool = False,
                 muted: bool = False,
                 loop: bool = False,
                 ) -> None:
        """Audio

        Args:
        
            - src (Union[str, Path]): The URL or local file path of the audio source.
            - controls (bool, optional): Whether to show the audio controls, like play, pause, and volume. Defaults to True.
            - autoplay (bool, optional): Whether to start playing the audio automatically. Defaults to False.
            - muted (bool, optional): Whether the audio should be initially muted. Defaults to False.
            - loop (bool, optional): Whether the audio should loop. Defaults to False.
            
        See [here ](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio#events)
        for a list of events you can subscribe to using the generic event subscription `on()`.
        """
        super().__init__(source=src)
        self._props['controls'] = controls
        self._props['autoplay'] = autoplay
        self._props['muted'] = muted
        self._props['loop'] = loop

    def seek(self, seconds: float) -> None:
            """
            Seek to a specific position in the audio.

            This method allows you to seek to a specific position in the audio file.
            It takes the number of seconds as input and moves the playback position to that position.

            Args:
                - seconds (float): The position in seconds.

            Example:
                To seek to the 30-second mark in the audio, you can use the following code:

                ```python
                audio.seek(30.0)
                ```
            """
            self.run_method('seek', seconds)

    def play(self) -> None:
        """Play the audio.

        This method plays the audio associated with the element.
        
        Usage:
            audio_element.play()
        
        Returns:
            None
        """
        self.run_method('play')

    def pause(self) -> None:
            """
            Pause the audio.

            This method pauses the audio playback. It sends a command to the audio element to pause the currently playing audio.

            Usage:
                audio_element.pause()

            Returns:
                None

            Raises:
                None
            """
            self.run_method('pause')
            