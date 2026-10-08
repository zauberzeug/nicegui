import math

from ..scene_object3d import Object3D


class Torus(Object3D, component='torus.js'):
    def __init__(
        self,
        radius: float = 1.0,
        tube: float = 0.4,
        radial_segments: int = 12,
        tubular_segments: int = 48,
        arc: float = 2 * math.pi,
        wireframe: bool = False,
    ) -> None:
        """Torus

        This element is based on Three.js' `TorusGeometry <https://threejs.org/docs/index.html#api/en/geometries/TorusGeometry>`_ object.
        It is used to create a donut-shaped mesh.

        :param radius: radius from the center of the torus to the center of the tube (default: 1.0)
        :param tube: radius of the tube (default: 0.4)
        :param radial_segments: number of segments along the tube cross-section (default: 12)
        :param tubular_segments: number of segments along the tube length (default: 48)
        :param arc: central angle of the torus in radians (default: 2π)
        :param wireframe: whether to display the torus as a wireframe (default: `False`)
        """
        super().__init__(radius, tube, radial_segments, tubular_segments, arc, wireframe=wireframe)
