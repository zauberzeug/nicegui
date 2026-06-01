# 3D Scene Custom Objects

Plug a custom `THREE.Object3D` into `ui.scene` by pairing a JS component module
with an `Object3D` subclass.

## Contract

The Python side subclasses `Object3D` and declares the companion JS module via
the `component=` class kwarg. The path is resolved relative to the Python
source file:

```python
from typing_extensions import Self
from nicegui.elements.scene.scene_object3d import Object3D


class PulsingSphere(Object3D, component='pulsing_sphere.js'):
    def __init__(self, radius: float = 1.0) -> None:
        super().__init__(radius)

    def set_scale(self, s: float) -> Self:
        self.run_method('set_scale', s)
        return self
```

Arguments passed to `super().__init__(...)` are forwarded positionally to the
JS-side factory. Any additional Python method can dispatch to a JS-side method
of the same name via `self.run_method('<method_name>', *args)`.

The JS module's default export is a class. The framework instantiates it once
per scene object and calls one of two entry points to build the mesh:

- `create_geometry(...args)` — return a `THREE.BufferGeometry`. The framework
  wraps it in a `MeshPhongMaterial` (or a wireframe `LineSegments`) and feeds
  the built-in `material()` / `scale()` / `move()` controls automatically.
- `create_mesh(...args)` — return a `THREE.Object3D` outright. Use this when
  you need ongoing access to the mesh from your own methods (store it on
  `this.mesh`), or when the mesh is complex and cannot be represented with
  just a `THREE.BufferGeometry`.

Optional hooks the framework will call if you define them:

- `apply_material(color, opacity, side)` — override the default material
  handling (useful for groups/GLTF where multiple sub-meshes exist).
- `attached(scene, parent_mesh)` — after the mesh is added to its parent.
- `detached(scene)` — after the mesh is removed from its parent.
- `deleted()` — after the object is deleted.

```js
import SceneLib from "nicegui-scene";
const { THREE } = SceneLib;

export default class PulsingSphere {
  mesh;

  create_mesh(radius) {
    const geometry = new THREE.SphereGeometry(radius, 32, 16);
    const material = new THREE.MeshPhongMaterial({ color: 0x44aaff, transparent: true });
    this.mesh = new THREE.Mesh(geometry, material);
    return this.mesh;
  }

  set_scale(s) {
    this.mesh.scale.set(s, s, s);
  }
}
```

Run with: `uv run main.py`.

![Screenshot](screenshot.webp)
