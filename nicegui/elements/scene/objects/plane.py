from ..scene_object3d import Object3D


class Plane(Object3D, component='plane.js'):
    def __init__(
        self,
        width: float = 1.0,
        height: float = 1.0,
        width_segments: int = 1,
        height_segments: int = 1,
        wireframe: bool = False,
    ) -> None:
        """Plane

        This element is based on Three.js' `PlaneGeometry <https://threejs.org/docs/index.html#api/en/geometries/PlaneGeometry>`_ object.
        It is used to create a flat rectangular mesh.

        :param width: width of the plane (default: 1.0)
        :param height: height of the plane (default: 1.0)
        :param width_segments: number of segments along the width (default: 1)
        :param height_segments: number of segments along the height (default: 1)
        :param wireframe: whether to display the plane as a wireframe (default: `False`)
        """
        super().__init__(width, height, width_segments, height_segments, wireframe=wireframe)
