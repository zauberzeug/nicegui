from ..scene_object3d import Object3D


class Text(Object3D, component='text.js'):
    def __init__(
        self,
        text: str,
        style: str = '',
    ) -> None:
        """Text

        This element is used to add 2D text to the scene.
        It can be moved like any other object, but always faces the camera.

        :param text: text to display
        :param style: CSS style (default: '')
        """
        super().__init__(text, style)
