
from ..scene_object3d import Object3D


class Stl(Object3D, component='stl.js'):
    def __init__(
        self,
        url: str,
        wireframe: bool = False,
    ) -> None:
        """STL

        This element is used to create a mesh from an STL file.

        :param url: URL of the STL file
        :param wireframe: whether to display the STL as a wireframe (default: `False`)
        """
        super().__init__(url, wireframe)
