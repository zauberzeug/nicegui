from ...dependencies import setup_esm_package

__getattr__, __dir__ = setup_esm_package(__file__, __name__, 'nicegui-scene', {
    'Scene': '.scene',
    'SceneCamera': '.scene',
    'SceneObject': '.scene',
    'Object3D': '.scene_object3d',
    'SceneView': '.scene_view',
})
__all__ = ['Object3D', 'Scene', 'SceneCamera', 'SceneObject', 'SceneView']  # pylint: disable=undefined-all-variable
