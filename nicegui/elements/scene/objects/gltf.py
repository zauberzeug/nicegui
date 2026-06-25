from ..scene_object3d import Object3D


class Gltf(Object3D, component='gltf.js'):
    def __init__(
        self,
        url: str,
    ) -> None:
        """GLTF

        This element is used to create a mesh from a glTF file.

        :param url: URL of the glTF file
        """
        super().__init__(url)
