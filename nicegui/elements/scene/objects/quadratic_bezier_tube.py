from ..scene_object3d import Object3D


class QuadraticBezierTube(Object3D, component='quadratic_bezier_tube.js'):
    def __init__(
        self,
        start: list[float],
        mid: list[float],
        end: list[float],
        tubular_segments: int = 64,
        radius: float = 1.0,
        radial_segments: int = 8,
        closed: bool = False,
        wireframe: bool = False,
    ) -> None:
        """Quadratic Bezier Tube

        This element is based on Three.js' `QuadraticBezierCurve3 <https://threejs.org/docs/index.html#api/en/extras/curves/QuadraticBezierCurve3>`_ object.
        It is used to create a tube-shaped mesh.

        :param start: start point of the curve
        :param mid: middle point of the curve
        :param end: end point of the curve
        :param tubular_segments: number of tubular segments (default: 64)
        :param radius: radius of the tube (default: 1.0)
        :param radial_segments: number of radial segments (default: 8)
        :param closed: whether the tube should be closed (default: `False`)
        :param wireframe: whether to display the tube as a wireframe (default: `False`)
        """
        super().__init__(
            start, mid, end, tubular_segments, radius, radial_segments, closed, wireframe
        )
