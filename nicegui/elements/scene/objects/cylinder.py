
from ..scene_object3d import Object3D


class Cylinder(Object3D, component='cylinder.js'):
    def __init__(
        self,
        top_radius: float = 1.0,
        bottom_radius: float = 1.0,
        height: float = 1.0,
        radial_segments: int = 8,
        height_segments: int = 1,
        wireframe: bool = False,
    ) -> None:
        """Cylinder

        This element is based on Three.js' `CylinderGeometry <https://threejs.org/docs/index.html#api/en/geometries/CylinderGeometry>`_ object.
        It is used to create a cylinder-shaped mesh.

        :param top_radius: radius of the top (default: 1.0)
        :param bottom_radius: radius of the bottom (default: 1.0)
        :param height: height of the cylinder (default: 1.0)
        :param radial_segments: number of horizontal segments (default: 8)
        :param height_segments: number of vertical segments (default: 1)
        :param wireframe: whether to display the cylinder as a wireframe (default: `False`)
        """
        super().__init__(top_radius, bottom_radius, height, radial_segments, height_segments, wireframe)
