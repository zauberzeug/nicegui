from ..scene_object3d import Object3D


class Sphere(Object3D, component='sphere.js'):
    def __init__(
        self,
        radius: float = 1.0,
        width_segments: int = 32,
        height_segments: int = 16,
        wireframe: bool = False,
    ) -> None:
        """Sphere

        This element is based on Three.js' `SphereGeometry <https://threejs.org/docs/index.html#api/en/geometries/SphereGeometry>`_ object.
        It is used to create a sphere-shaped mesh.

        :param radius: radius of the sphere (default: 1.0)
        :param width_segments: number of horizontal segments (default: 32)
        :param height_segments: number of vertical segments (default: 16)
        :param wireframe: whether to display the sphere as a wireframe (default: `False`)
        """
        super().__init__(radius, width_segments, height_segments, wireframe)
