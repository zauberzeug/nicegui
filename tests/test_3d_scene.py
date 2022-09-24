from nicegui import ui

from .user import User


def test_moving_sphere_with_timer(user: User):
    with ui.scene() as scene:
        sphere = scene.sphere().move(0, -5, 2)
        ui.timer(0.03, lambda: sphere.move(sphere.x, sphere.y + 0.05, sphere.z))

    user.open('/')
    user.sleep(0.1)
    def position(): return user.selenium.execute_script('return scene.children[4].position.y')
    pos = position()
    user.sleep(0.1)
    assert position() > pos
