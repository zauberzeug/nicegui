from nicegui import ui

from . import doc


@doc.demo(ui.scene)
def main_demo() -> None:
    with ui.scene().classes('w-full h-64') as scene:
        scene.sphere().material('#4488ff')
        scene.cylinder(1, 0.5, 2, 20).material('#ff8800', opacity=0.5).move(-2, 1)
        scene.extrusion([[0, 0], [0, 1], [1, 0.5]], 0.1).material('#ff8888').move(2, -1)

        with scene.group().move(z=2):
            scene.box().move(x=2)
            scene.box().move(y=2).rotate(0.25, 0.5, 0.75)
            scene.box(wireframe=True).material('#888888').move(x=2, y=2)

        scene.line([-4, 0, 0], [-4, 2, 0]).material('#ff0000')
        scene.curve([-4, 0, 0], [-4, -1, 0], [-3, -1, 0], [-3, 0, 0]).material('#008800')

        logo = 'https://avatars.githubusercontent.com/u/2843826'
        scene.texture(logo, [[[0.5, 2, 0], [2.5, 2, 0]],
                             [[0.5, 0, 0], [2.5, 0, 0]]]).move(1, -3)

        teapot = 'https://upload.wikimedia.org/wikipedia/commons/9/93/Utah_teapot_(solid).stl'
        scene.stl(teapot).scale(0.2).move(-3, 4)

        avocado = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models/Avocado/glTF-Binary/Avocado.glb'
        scene.gltf(avocado).scale(40).move(-2, -3, 0.5)

        scene.text('2D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(z=2)
        scene.text3d('3D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(y=-2).scale(.05)


@doc.demo('Handling Click Events', '''
    You can use the `on_click` argument to `ui.scene` to handle click events.
    The callback receives a `SceneClickEventArguments` object with the following attributes:

    - `click_type`: the type of click ("click" or "dblclick").
    - `button`: the button that was clicked (1, 2, or 3).
    - `alt`, `ctrl`, `meta`, `shift`: whether the alt, ctrl, meta, or shift key was pressed.
    - `hits`: a list of `SceneClickEventHit` objects, sorted by distance from the camera.

    The `SceneClickEventHit` object has the following attributes:

    - `object_id`: the id of the object that was clicked.
    - `object_name`: the name of the object that was clicked.
    - `x`, `y`, `z`: the x, y and z coordinates of the click.
''')
def click_events() -> None:
    from nicegui import events

    def handle_click(e: events.SceneClickEventArguments):
        hit = e.hits[0]
        name = hit.object_name or hit.object_id
        ui.notify(f'You clicked on the {name} at ({hit.x:.2f}, {hit.y:.2f}, {hit.z:.2f})')

    with ui.scene(width=285, height=220, on_click=handle_click) as scene:
        scene.sphere().move(x=-1, z=1).with_name('sphere')
        scene.box().move(x=1, z=1).with_name('box')


@doc.demo('Draggable objects', '''
    You can make objects draggable using the `.draggable` method.
    There is an optional `on_drag_start` and `on_drag_end` argument to `ui.scene` to handle drag events.
    The callbacks receive a `SceneDragEventArguments` object with the following attributes:

    - `type`: the type of drag event ("dragstart" or "dragend").
    - `object_id`: the id of the object that was dragged.
    - `object_name`: the name of the object that was dragged.
    - `x`, `y`, `z`: the x, y and z coordinates of the dragged object.

    You can also use the `drag_constraints` argument to set comma-separated JavaScript expressions
    for constraining positions of dragged objects.
''')
def draggable_objects() -> None:
    from nicegui import events

    def handle_drag(e: events.SceneDragEventArguments):
        ui.notify(f'You dropped the sphere at ({e.x:.2f}, {e.y:.2f}, {e.z:.2f})')

    with ui.scene(width=285, height=220,
                  drag_constraints='z = 1', on_drag_end=handle_drag) as scene:
        sphere = scene.sphere().move(z=1).draggable()

    ui.switch('draggable sphere',
              value=sphere.draggable_,
              on_change=lambda e: sphere.draggable(e.value))


@doc.demo('Rendering point clouds', '''
    You can render point clouds using the `point_cloud` method.
    The `points` argument is a list of point coordinates, and the `colors` argument is a list of RGB colors (0..1).
''')
def point_clouds() -> None:
    import numpy as np

    with ui.scene().classes('w-full h-64') as scene:
        x, y = np.meshgrid(np.linspace(-3, 3), np.linspace(-3, 3))
        z = np.sin(x) * np.cos(y) + 1
        points = np.dstack([x, y, z]).reshape(-1, 3)
        scene.point_cloud(points=points, colors=points, point_size=0.1)


@doc.demo('Wait for Initialization', '''
    You can wait for the scene to be initialized with the `initialized` method.
    This demo animates a camera movement after the scene has been fully loaded.
''')
async def wait_for_init() -> None:
    with ui.scene(width=285, height=220) as scene:
        scene.sphere()
        await scene.initialized()
        scene.move_camera(x=1, y=-1, z=1.5, duration=2)


@doc.demo('Camera Parameters', '''
    You can use the `camera` argument to `ui.scene` to use a custom camera.
    This allows you to set the field of view of a perspective camera or the size of an orthographic camera.
''')
def orthographic_camera() -> None:
    with ui.scene(camera=ui.scene.orthographic_camera(size=2)) \
            .classes('w-full h-64') as scene:
        scene.box()


doc.reference(ui.scene)
