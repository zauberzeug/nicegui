from ..scene_object3d import Object3D


class Line(Object3D, component='line.js'):
    def __init__(
        self,
        start: list[float],
        end: list[float],
    ) -> None:
        """Line

        This element is based on Three.js' `Line <https://threejs.org/docs/index.html#api/en/objects/Line>`_ object.
        It is used to create a line segment.

        :param start: start point of the line
        :param end: end point of the line
        """
        super().__init__(start, end)
