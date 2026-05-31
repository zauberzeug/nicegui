import math

from ..scene_object3d import Object3D


class Ring(Object3D, component='ring.js'):
    def __init__(
        self,
        inner_radius: float = 0.5,
        outer_radius: float = 1.0,
        theta_segments: int = 8,
        phi_segments: int = 1,
        theta_start: float = 0,
        theta_length: float = 2 * math.pi,
        wireframe: bool = False,
    ) -> None:
        """Ring

        This element is based on Three.js' `RingGeometry <https://threejs.org/docs/index.html#api/en/geometries/RingGeometry>`_ object.
        It is used to create a ring-shaped mesh.

        :param inner_radius: inner radius of the ring (default: 0.5)
        :param outer_radius: outer radius of the ring (default: 1.0)
        :param theta_segments: number of horizontal segments (default: 8, higher means rounder)
        :param phi_segments: number of vertical segments (default: 1)
        :param theta_start: start angle in radians (default: 0)
        :param theta_length: central angle in radians (default: 2π)
        :param wireframe: whether to display the ring as a wireframe (default: `False`)
        """
        super().__init__(
            'ring', inner_radius, outer_radius, theta_segments, phi_segments, theta_start, theta_length, wireframe
        )
