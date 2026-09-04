from typing import TYPE_CHECKING

from ...dependencies import setup_esm_package

__getattr__, __dir__ = setup_esm_package(__file__, __name__, 'nicegui-scene', {
    'Object3D': '.scene_object3d',
    'Scene': '.scene',
    'SceneCamera': '.scene',
    'SceneObject': '.scene',
    'SceneView': '.scene_view',
})
__all__ = ['Object3D', 'Scene', 'SceneCamera', 'SceneObject', 'SceneView']

if TYPE_CHECKING:
    from .scene import Scene, SceneCamera, SceneObject
    from .scene_object3d import Object3D
    from .scene_view import SceneView
