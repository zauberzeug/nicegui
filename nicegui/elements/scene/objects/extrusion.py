from ..scene_object3d import Object3D


class Extrusion(Object3D, component='extrusion.js'):
    def __init__(
        self,
        outline: list[list[float]],
        height: float,
        wireframe: bool = False,
    ) -> None:
        """Extrusion

        This element is based on Three.js' `ExtrudeGeometry <https://threejs.org/docs/index.html#api/en/geometries/ExtrudeGeometry>`_ object.
        It is used to create a 3D shape by extruding a 2D shape to a given height.

        :param outline: list of points defining the outline of the 2D shape
        :param height: height of the extrusion
        :param wireframe: whether to display the extrusion as a wireframe (default: `False`)
        """
        super().__init__(outline, height, wireframe)
