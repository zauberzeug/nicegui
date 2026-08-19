from ..scene_object3d import Object3D


class Capsule(Object3D, component='capsule.js'):
    def __init__(
        self,
        radius: float = 1.0,
        length: float = 1.0,
        cap_segments: int = 4,
        radial_segments: int = 8,
        height_segments: int = 1,
        wireframe: bool = False,
    ) -> None:
        """Capsule

        This element is based on Three.js' `CapsuleGeometry <https://threejs.org/docs/index.html#api/en/geometries/CapsuleGeometry>`_ object.
        It is used to create a capsule-shaped mesh (a cylinder with hemispherical caps).

        :param radius: radius of the capsule (default: 1.0)
        :param length: length of the cylindrical middle section (default: 1.0)
        :param cap_segments: number of segments used to draw each cap (default: 4)
        :param radial_segments: number of segments around the circumference (default: 8)
        :param height_segments: number of segments along the cylindrical section (default: 1)
        :param wireframe: whether to display the capsule as a wireframe (default: `False`)
        """
        super().__init__(radius, length, cap_segments, radial_segments, height_segments,
                         wireframe=wireframe)
