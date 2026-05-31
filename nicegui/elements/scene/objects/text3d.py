from ..scene_object3d import Object3D


class Text3d(Object3D, component='text3d.js'):
    def __init__(
        self,
        text: str,
        style: str = '',
    ) -> None:
        """3D Text

        This element is used to add a 3D text mesh to the scene.
        It can be moved and rotated like any other object.

        :param text: text to display
        :param style: CSS style (default: '')
        """
        super().__init__(text, style)
