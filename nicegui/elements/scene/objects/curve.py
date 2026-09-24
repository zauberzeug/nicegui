from ..scene_object3d import Object3D


class Curve(Object3D, component='curve.js'):
    def __init__(
        self,
        start: list[float],
        control1: list[float],
        control2: list[float],
        end: list[float],
        num_points: int = 20,
    ) -> None:
        """Curve

        This element is based on Three.js' `CubicBezierCurve3 <https://threejs.org/docs/index.html#api/en/extras/curves/CubicBezierCurve3>`_ object.

        :param start: start point of the curve
        :param control1: first control point of the curve
        :param control2: second control point of the curve
        :param end: end point of the curve
        :param num_points: number of points to use for the curve (default: 20)
        """
        super().__init__(start, control1, control2, end, num_points)
