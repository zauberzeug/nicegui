from typing_extensions import Self

from ..scene_object3d import Object3D


class Texture(Object3D, component='texture.js'):
    def __init__(
        self,
        url: str,
        coordinates: list[list[list[float] | None]],
    ) -> None:
        """Texture

        This element is used to add a texture to a mesh.

        :param url: URL of the texture image
        :param coordinates: texture coordinates
        """
        super().__init__(url, coordinates)

    def set_url(self, url: str) -> Self:
        """Change the URL of the texture image."""
        self.args[0] = url
        self.run_method('set_url', self.id, url)
        return self

    def set_coordinates(self, coordinates: list[list[list[float] | None]]) -> Self:
        """Change the texture coordinates."""
        self.args[1] = coordinates
        self.run_method('set_coordinates', self.id, coordinates)
        return self
