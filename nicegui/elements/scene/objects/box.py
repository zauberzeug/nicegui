from ..scene_object3d import Object3D


class Box(Object3D, component='box.js'):
    def __init__(
        self,
        width: float = 1.0,
        height: float = 1.0,
        depth: float = 1.0,
        wireframe: bool = False,
    ) -> None:
        """Box

        This element is based on Three.js' `BoxGeometry <https://threejs.org/docs/index.html#api/en/geometries/BoxGeometry>`_ object.
        It is used to create a box-shaped mesh.

        :param width: width of the box (default: 1.0)
        :param height: height of the box (default: 1.0)
        :param depth: depth of the box (default: 1.0)
        :param wireframe: whether to display the box as a wireframe (default: `False`)
        """
        super().__init__(width, height, depth, wireframe)
