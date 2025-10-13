import pytest

from nicegui.testing import Screen, User


@pytest.mark.xfail(raises=FileNotFoundError)
@pytest.mark.nicegui_test(main_file='non_existent_file.py')
async def test_marker_injects_main_file_for_user_plugin(user: User):
    """Ensures that the nicegui_test marker injects the main file correctly
    by trying to load a non-existent file and expecting a FileNotFoundError.
    """
    await user.open('/')

@pytest.mark.xfail(raises=FileNotFoundError)
@pytest.mark.nicegui_test(main_file='non_existent_file.py')
def test_marker_injects_main_file_for_screen_plugin(screen: Screen):
    """Ensures that the nicegui_test marker injects the main file correctly
    by trying to load a non-existent file and expecting a FileNotFoundError.
    """
    screen.open('/')
