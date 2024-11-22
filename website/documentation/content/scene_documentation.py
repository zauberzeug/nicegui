from nicegui import ui

from . import doc


@doc.demo(ui.scene)
def main_demo() -> None:
    with ui.scene().classes('w-full h-64') as scene:
        scene.axes_helper()
        scene.sphere().material('#4488ff').move(2, 2)
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


@doc.demo('Context menu for 3D objects', '''
    This demo shows how to create a context menu for 3D objects.
    By setting the `click_events` argument to `['contextmenu']`, the `handle_click` function will be called on right-click.
    It clears the context menu and adds items based on the object that was clicked.
''')
def context_menu_for_3d_objects():
    from nicegui import events

    def handle_click(e: events.SceneClickEventArguments) -> None:
        context_menu.clear()
        name = next((hit.object_name for hit in e.hits if hit.object_name), None)
        with context_menu:
            if name == 'sphere':
                ui.item('SPHERE').classes('font-bold')
                ui.menu_item('inspect')
                ui.menu_item('open')
            if name == 'box':
                ui.item('BOX').classes('font-bold')
                ui.menu_item('rotate')
                ui.menu_item('move')

    with ui.element():
        context_menu = ui.context_menu()
        with ui.scene(width=285, height=220, on_click=handle_click,
                      click_events=['contextmenu']) as scene:
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


@doc.demo('Subscribe to the drag event', '''
    By default, a draggable object is only updated when the drag ends to avoid performance issues.
    But you can explicitly subscribe to the "drag" event to get immediate updates.
    In this demo we update the position and size of a box based on the positions of two draggable spheres.
''')
def immediate_updates() -> None:
    from nicegui import events

    with ui.scene(width=285, drag_constraints='z=0') as scene:
        box = scene.box(1, 1, 0.2).move(0, 0).material('Orange')
        sphere1 = scene.sphere(0.2).move(0.5, -0.5).material('SteelBlue').draggable()
        sphere2 = scene.sphere(0.2).move(-0.5, 0.5).material('SteelBlue').draggable()

    def handle_drag(e: events.GenericEventArguments) -> None:
        x1 = sphere1.x if e.args['object_id'] == sphere2.id else e.args['x']
        y1 = sphere1.y if e.args['object_id'] == sphere2.id else e.args['y']
        x2 = sphere2.x if e.args['object_id'] == sphere1.id else e.args['x']
        y2 = sphere2.y if e.args['object_id'] == sphere1.id else e.args['y']
        box.move((x1 + x2) / 2, (y1 + y2) / 2).scale(x2 - x1, y2 - y1, 1)
    scene.on('drag', handle_drag)


@doc.demo('Rendering point clouds', '''
    You can render point clouds using the `point_cloud` method.
    The `points` argument is a list of point coordinates, and the `colors` argument is a list of RGB colors (0..1).
    You can update the cloud using its `set_points()` method.
''')
def point_clouds() -> None:
    import numpy as np

    def generate_data(frequency: float = 1.0):
        x, y = np.meshgrid(np.linspace(-3, 3), np.linspace(-3, 3))
        z = np.sin(x * frequency) * np.cos(y * frequency) + 1
        points = np.dstack([x, y, z]).reshape(-1, 3)
        colors = points / [6, 6, 2] + [0.5, 0.5, 0]
        return points, colors

    with ui.scene().classes('w-full h-64') as scene:
        points, colors = generate_data()
        point_cloud = scene.point_cloud(points, colors, point_size=0.1)

    ui.slider(min=0.1, max=3, step=0.1, value=1) \
        .on_value_change(lambda e: point_cloud.set_points(*generate_data(e.value)))


@doc.demo('Wait for Initialization', '''
    You can wait for the scene to be initialized with the `initialized` method.
    This demo animates a camera movement after the scene has been fully loaded.
''')
async def wait_for_init() -> None:
    # @ui.page('/')
    # async def page():
    with ui.column():  # HIDE
        with ui.scene(width=285, height=220) as scene:
            scene.sphere()
            await scene.initialized()
            scene.move_camera(x=1, y=-1, z=1.5, duration=2)


@doc.demo(ui.scene_view)
def scene_views():
    with ui.grid(columns=2).classes('w-full'):
        with ui.scene().classes('h-64 col-span-2') as scene:
            teapot = 'https://upload.wikimedia.org/wikipedia/commons/9/93/Utah_teapot_(solid).stl'
            scene.stl(teapot).scale(0.3)

        with ui.scene_view(scene).classes('h-32') as scene_view1:
            scene_view1.move_camera(x=1, y=-3, z=5)

        with ui.scene_view(scene).classes('h-32') as scene_view2:
            scene_view2.move_camera(x=0, y=4, z=3)


@doc.demo('Camera Parameters', '''
    You can use the `camera` argument to `ui.scene` to use a custom camera.
    This allows you to set the field of view of a perspective camera or the size of an orthographic camera.
''')
def orthographic_camera() -> None:
    with ui.scene(camera=ui.scene.orthographic_camera(size=2)) \
            .classes('w-full h-64') as scene:
        scene.box()


@doc.demo('Get current camera pose', '''
    Using the `get_camera` method you can get a dictionary of current camera parameters like position, rotation, field of view and more.
    This demo shows how to continuously move a sphere towards the camera.
    Try moving the camera around to see the sphere following it.
''')
def camera_pose() -> None:
    with ui.scene().classes('w-full h-64') as scene:
        ball = scene.sphere()

    async def move():
        camera = await scene.get_camera()
        if camera is not None:
            ball.move(x=0.95 * ball.x + 0.05 * camera['position']['x'],
                      y=0.95 * ball.y + 0.05 * camera['position']['y'],
                      z=1.0)
    ui.timer(0.1, move)


@doc.demo('Custom Background', '''
    You can set a custom background color using the `background_color` parameter of `ui.scene`.
''')
def custom_background() -> None:
    with ui.scene(background_color='#222').classes('w-full h-64') as scene:
        scene.box()


@doc.demo('Custom Grid', '''
    You can set custom grid parameters using the `grid` parameter of `ui.scene`.
    It accepts a tuple of two integers, the first one for the grid size and the second one for the number of divisions.
''')
def custom_grid() -> None:
    with ui.scene(grid=(3, 2)).classes('w-full h-64') as scene:
        scene.sphere()


@doc.demo('Custom Composed 3D Objects', '''
    This demo creates a custom class for visualizing a coordinate system with colored X, Y and Z axes.
    This can be a nice alternative to the default `axes_helper` object.
''')
def custom_composed_objects() -> None:
    import math

    class CoordinateSystem(ui.scene.group):

        def __init__(self, name: str, *, length: float = 1.0) -> None:
            super().__init__()

            with self:
                for label, color, rx, ry, rz in [
                    ('x', '#ff0000', 0, 0, -math.pi / 2),
                    ('y', '#00ff00', 0, 0, 0),
                    ('z', '#0000ff', math.pi / 2, 0, 0),
                ]:
                    with ui.scene.group().rotate(rx, ry, rz):
                        ui.scene.cylinder(0.02 * length, 0.02 * length, 0.8 * length) \
                            .move(y=0.4 * length).material(color)
                        ui.scene.cylinder(0, 0.1 * length, 0.2 * length) \
                            .move(y=0.9 * length).material(color)
                        ui.scene.text(label, style=f'color: {color}') \
                            .move(y=1.1 * length)
                ui.scene.text(name, style='color: #808080')

    with ui.scene().classes('w-full h-64'):
        CoordinateSystem('origin')
        CoordinateSystem('custom frame').move(-2, -2, 1).rotate(0.1, 0.2, 0.3)


@doc.demo('Attaching/detaching objects', '''
    To add or remove objects from groups you can use the `attach` and `detach` methods.
    The position and rotation of the object are preserved so that the object does not move in space.
    But note that scaling is not preserved.
    If either the parent or the object itself is scaled, the object shape and position can change.
''')
def attach_detach() -> None:
    import math
    import time

    with ui.scene().classes('w-full h-64') as scene:
        with scene.group() as group:
            a = scene.box().move(-2)
            b = scene.box().move(0)
            c = scene.box().move(2)

    ui.timer(0.1, lambda: group.move(y=math.sin(time.time())).rotate(0, 0, time.time()))
    ui.button('Detach', on_click=a.detach)
    ui.button('Attach', on_click=lambda: a.attach(group))


doc.reference(ui.scene)
