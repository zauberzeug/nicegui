from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    with ui.scene().classes('w-full h-64') as scene:
        scene.sphere().material('#4488ff')
        scene.cylinder(1, 0.5, 2, 20).material('#ff8800', opacity=0.5).move(-2, 1)
        scene.extrusion([[0, 0], [0, 1], [1, 0.5]], 0.1).material('#ff8888').move(-2, -2)

        with scene.group().move(z=2):
            scene.box().move(x=2)
            scene.box().move(y=2).rotate(0.25, 0.5, 0.75)
            scene.box(wireframe=True).material('#888888').move(x=2, y=2)

        scene.line([-4, 0, 0], [-4, 2, 0]).material('#ff0000')
        scene.curve([-4, 0, 0], [-4, -1, 0], [-3, -1, 0], [-3, -2, 0]).material('#008800')

        logo = 'https://avatars.githubusercontent.com/u/2843826'
        scene.texture(logo, [[[0.5, 2, 0], [2.5, 2, 0]],
                             [[0.5, 0, 0], [2.5, 0, 0]]]).move(1, -2)

        teapot = 'https://upload.wikimedia.org/wikipedia/commons/9/93/Utah_teapot_(solid).stl'
        scene.stl(teapot).scale(0.2).move(-3, 4)

        scene.text('2D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(z=2)
        scene.text3d('3D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(y=-2).scale(.05)


def more() -> None:
    @text_demo('Handling Click Events', '''
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
