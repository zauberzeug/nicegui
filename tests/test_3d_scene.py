from nicegui import ui
from selenium.common.exceptions import JavascriptException

from .screen import Screen


def test_moving_sphere_with_timer(screen: Screen):
    with ui.scene() as scene:
        sphere = scene.sphere().move(0, -5, 2)
        ui.timer(0.03, lambda: sphere.move(sphere.x, sphere.y + 0.05, sphere.z))

    screen.open('/')

    def position():
        for i in range(5):
            try:
                return screen.selenium.execute_script('return scene.children[4].position.y')
            except JavascriptException:
                screen.wait(0.1)

    pos = position()
    screen.wait(0.1)
    assert position() > pos
