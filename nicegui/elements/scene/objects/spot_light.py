import math

from ..scene_object3d import Object3D


class SpotLight(Object3D, component='spot_light.js'):
    def __init__(
        self,
        color: str = '#ffffff',
        intensity: float = 1.0,
        distance: float = 0.0,
        angle: float = math.pi / 3,
        penumbra: float = 0.0,
        decay: float = 1.0,
    ) -> None:
        """Spot Light

        This element is based on Three.js' `SpotLight <https://threejs.org/docs/index.html#api/en/lights/SpotLight>`_ object.
        It is used to add a spot light to the scene.

        :param color: CSS color string (default: '#ffffff')
        :param intensity: light intensity (default: 1.0)
        :param distance: maximum distance of light (default: 0.0)
        :param angle: maximum angle of light (default: π/2)
        :param penumbra: penumbra (default: 0.0)
        :param decay: decay (default: 2.0)
        """
        super().__init__(color, intensity, distance, angle, penumbra, decay)
