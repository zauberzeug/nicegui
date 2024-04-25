from typing import Optional

from nicegui import ui
from nicegui.testing import Screen


def test_create_dynamically(screen: Screen):
    scene = ui.scene()
    scene_view: Optional[ui.scene_view] = None

    def create():
        nonlocal scene_view
        scene_view = ui.scene_view(scene)
    ui.button('Create', on_click=create)

    screen.open('/')
    screen.click('Create')
    assert scene_view is not None
    assert screen.selenium.execute_script(f'return getElement({scene_view.id}).scene == getElement({scene.id})')


def test_object_creation_via_context(screen: Screen):
    with ui.scene() as scene:
        scene.box().with_name('box')

    scene_view = ui.scene_view(scene)

    screen.open('/')
    screen.wait(0.5)
    assert screen.selenium.execute_script(f'return getElement({scene_view.id}).scene == getElement({scene.id})')
