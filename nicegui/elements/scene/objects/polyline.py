from ..scene_object3d import Object3D


class Polyline(Object3D, component='polyline.js'):
    def __init__(
        self,
        points: list[list[float]],
        colors: list[list[float]] | None = None,
        dashed: bool = False,
        dash_size: float = 0.1,
        gap_size: float = 0.05,
    ) -> None:
        """Polyline

        This element is based on Three.js' `Line <https://threejs.org/docs/#api/en/objects/Line>`_ object.
        It connects a sequence of 3D points with line segments and optionally dashes them via
        `LineDashedMaterial <https://threejs.org/docs/#api/en/materials/LineDashedMaterial>`_.

        :param points: list of ``[x, y, z]`` points
        :param colors: optional list of per-vertex ``[r, g, b]`` colors (each component in ``[0, 1]``).
            When supplied, the line uses vertex colors instead of the material color.
        :param dashed: whether to use a dashed material (default: ``False``)
        :param dash_size: dash length in scene units (default: ``0.1``)
        :param gap_size: gap length in scene units (default: ``0.05``)
        """
        if len(points) < 2:
            raise ValueError(f'points must have at least 2 entries (got {len(points)})')
        if colors is not None and len(colors) != len(points):
            raise ValueError(f'colors length ({len(colors)}) must match points length ({len(points)})')
        super().__init__(points, colors, dashed, dash_size, gap_size)
        if colors is not None:
            self.material(color=None)
