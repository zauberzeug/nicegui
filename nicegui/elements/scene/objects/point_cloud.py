from typing_extensions import Self

from ..scene_object3d import Object3D


class PointCloud(Object3D, component='point_cloud.js'):
    def __init__(
        self,
        points: list[list[float]],
        colors: list[list[float]] | None = None,
        point_size: float = 1.0,
    ) -> None:
        """Point Cloud

        This element is based on Three.js' `Points <https://threejs.org/docs/index.html#api/en/objects/Points>`_ object.

        :param points: list of points
        :param colors: optional list of colors (one per point)
        :param point_size: size of the points (default: 1.0)
        """
        super().__init__(points, colors, point_size)
        if colors is not None:
            self.material(color=None)

    def set_points(self, points: list[list[float]], colors: list[list[float]] | None = None) -> Self:
        """Change the points and colors of the point cloud."""
        self.args[0] = points
        self.args[1] = colors
        self.run_method('set_points', points, colors)
        if colors is not None:
            self.material(color=None)
        return self
