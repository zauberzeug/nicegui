from selenium.common.exceptions import JavascriptException

from nicegui import ui

from .screen import Screen


def test_moving_sphere_with_timer(screen: Screen):
    with ui.scene() as scene:
        sphere = scene.sphere().with_name('sphere')
        ui.timer(0.1, lambda: sphere.move(0, 0, sphere.z + 0.01))

    screen.open('/')

    def position() -> None:
        for _ in range(3):
            try:
                pos = screen.selenium.execute_script(f'return scene_{scene.id}.getObjectByName("sphere").position.z')
                if pos is not None:
                    return pos
            except JavascriptException as e:
                print(e.msg, flush=True)
            screen.wait(1.0)
        raise Exception('Could not get position')

    screen.wait(0.2)
    assert position() > 0


def test_no_object_duplication_on_index_client(screen: Screen):
    with ui.scene() as scene:
        sphere = scene.sphere().move(0, -4, 0)
        ui.timer(0.1, lambda: sphere.move(0, sphere.y + 0.5, 0))

    screen.open('/')
    screen.wait(0.4)
    screen.switch_to(1)
    screen.open('/')
    screen.switch_to(0)
    screen.wait(0.2)
    assert screen.selenium.execute_script(f'return scene_{scene.id}.children.length') == 5


def test_no_object_duplication_with_page_builder(screen: Screen):
    @ui.page('/')
    def page():
        global scene
        with ui.scene() as scene:
            sphere = scene.sphere().move(0, -4, 0)
            ui.timer(0.1, lambda: sphere.move(0, sphere.y + 0.5, 0))

    screen.open('/')
    screen.wait(0.4)
    screen.switch_to(1)
    screen.open('/')
    screen.switch_to(0)
    screen.wait(0.2)
    assert screen.selenium.execute_script(f'return scene_{scene.id}.children.length') == 5
    screen.switch_to(1)
    assert screen.selenium.execute_script(f'return scene_{scene.id}.children.length') == 5


def test_deleting_group(screen: Screen):
    with ui.scene() as scene:
        with scene.group() as group:
            scene.sphere()
    ui.button('Delete group', on_click=group.delete)

    screen.open('/')
    screen.wait(0.5)
    assert len(scene.objects) == 2
    screen.click('Delete group')
    screen.wait(0.5)
    assert len(scene.objects) == 0


def test_replace_scene(screen: Screen):
    with ui.row() as container:
        with ui.scene() as scene:
            scene.sphere().with_name('sphere')

    def replace():
        container.clear()
        with container:
            nonlocal scene
            with ui.scene() as scene:
                scene.box().with_name('box')
    ui.button('Replace scene', on_click=replace)

    screen.open('/')
    screen.wait(0.5)
    assert screen.selenium.execute_script(f'return scene_{scene.id}.children[4].name') == 'sphere'
    screen.click('Replace scene')
    screen.wait(0.5)
    assert screen.selenium.execute_script(f'return scene_{scene.id}.children[4].name') == 'box'
