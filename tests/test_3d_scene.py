from nicegui import ui
from selenium.common.exceptions import JavascriptException

from .screen import Screen


def test_moving_sphere_with_timer(screen: Screen):
    with ui.scene() as scene:
        sphere = scene.sphere()
        ui.timer(0.1, lambda: sphere.move(0, 0, sphere.z + 0.01))

    screen.open('/')

    def position() -> None:
        for _ in range(20):
            try:
                pos = screen.selenium.execute_script('return scene.children[4].position.z')
                if pos is not None:
                    return pos
            except JavascriptException:
                pass
            screen.wait(0.1)
        raise Exception('Could not get position')

    screen.wait(0.2)
    assert position() > 0
