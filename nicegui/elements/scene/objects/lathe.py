import math

from ..scene_object3d import Object3D


class Lathe(Object3D, component='lathe.js'):
    def __init__(
        self,
        points: list[list[float]],
        segments: int = 12,
        phi_start: float = 0.0,
        phi_length: float = 2 * math.pi,
        wireframe: bool = False,
    ) -> None:
        """Lathe

        This element is based on Three.js' `LatheGeometry <https://threejs.org/docs/#api/en/geometries/LatheGeometry>`_ object.
        It creates a surface of revolution by rotating a 2D polyline around the y axis.

        :param points: list of 2D ``[x, y]`` points making up the profile (x ≥ 0)
        :param segments: number of segments around the circumference (default: 12)
        :param phi_start: starting angle in radians (default: 0.0)
        :param phi_length: angular extent in radians (default: ``2π``)
        :param wireframe: whether to render the mesh as wireframe (default: ``False``)
        """
        super().__init__(points, segments, phi_start, phi_length, wireframe=wireframe)
