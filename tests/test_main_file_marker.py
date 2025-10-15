import pytest

from nicegui.testing import Screen, User


@pytest.mark.xfail(raises=FileNotFoundError)
@pytest.mark.nicegui_main_file('non_existent_file.py')
async def test_marker_injects_main_file_for_user_plugin(user: User):
    await user.open('/')


@pytest.mark.xfail(raises=FileNotFoundError)
@pytest.mark.nicegui_main_file('non_existent_file.py')
def test_marker_injects_main_file_for_screen_plugin(screen: Screen):
    screen.open('/')
