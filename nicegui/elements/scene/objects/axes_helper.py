from ..scene_object3d import Object3D


class AxesHelper(Object3D, component='axes_helper.js'):
    def __init__(
        self,
        length: float = 1.0,
    ) -> None:
        """Axes Helper

        This element is based on Three.js' `AxesHelper <https://threejs.org/docs/#api/en/helpers/AxesHelper>`_ object.
        It is used to visualize the XYZ axes:
        The X axis is red.
        The Y axis is green.
        The Z axis is blue.

        :param length: length of the the axes (default: 1.0)
        """
        super().__init__(length)
