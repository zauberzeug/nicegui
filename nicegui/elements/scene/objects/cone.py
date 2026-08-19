import math

from ..scene_object3d import Object3D


class Cone(Object3D, component='cone.js'):
    def __init__(
        self,
        radius: float = 1.0,
        height: float = 1.0,
        radial_segments: int = 8,
        height_segments: int = 1,
        open_ended: bool = False,
        theta_start: float = 0,
        theta_length: float = 2 * math.pi,
        wireframe: bool = False,
    ) -> None:
        """Cone

        This element is based on Three.js' `ConeGeometry <https://threejs.org/docs/index.html#api/en/geometries/ConeGeometry>`_ object.
        It is used to create a cone-shaped mesh.

        :param radius: radius of the base (default: 1.0)
        :param height: height of the cone (default: 1.0)
        :param radial_segments: number of horizontal segments (default: 8)
        :param height_segments: number of vertical segments (default: 1)
        :param open_ended: whether the base is open (default: `False`)
        :param theta_start: start angle in radians (default: 0)
        :param theta_length: central angle in radians (default: 2π)
        :param wireframe: whether to display the cone as a wireframe (default: `False`)
        """
        super().__init__(radius, height, radial_segments, height_segments,
                         open_ended, theta_start, theta_length, wireframe=wireframe)
