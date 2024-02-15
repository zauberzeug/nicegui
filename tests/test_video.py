from nicegui import ui
from nicegui.testing import Screen

VIDEO1 = 'https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
VIDEO2 = 'https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4'


def test_replace_video(screen: Screen):
    """
    Test function to verify the behavior of replacing a video in a GUI.

    Args:
        screen (Screen): The screen object representing the GUI screen.

    Returns:
        None

    Raises:
        AssertionError: If the video replacement does not work as expected.

    Usage:
        1. Create a GUI screen using the `Screen` class.
        2. Call this function passing the created `Screen` object as an argument.
        3. The function will add a video element to the GUI screen.
        4. Clicking the "Replace" button will replace the video with a different one.
        5. The function will assert that the video replacement was successful.
    """
    with ui.row() as container:
        ui.video(VIDEO1)

    def replace():
        container.clear()
        with container:
            ui.video(VIDEO2)
    ui.button('Replace', on_click=replace)

    screen.open('/')
    assert screen.find_by_tag('video').get_attribute('src').endswith('BigBuckBunny.mp4')
    screen.click('Replace')
    screen.wait(0.5)
    assert screen.find_by_tag('video').get_attribute('src').endswith('ElephantsDream.mp4')


def test_change_source(screen: Screen):
    """
    Test the functionality of changing the video source in a NiceGUI application.

    Args:
        screen (Screen): The NiceGUI screen object.

    Raises:
        AssertionError: If the video source is not changed successfully.

    Usage:
        1. Create a NiceGUI screen object.
        2. Call this function passing the screen object as an argument.
        3. The function will create a video element with the initial source set to VIDEO1.
        4. It will also create a button labeled 'Change source' that triggers the change of the video source to VIDEO2.
        5. Open the screen using the `open()` method.
        6. Assert that the initial video source ends with 'BigBuckBunny.mp4'.
        7. Click the 'Change source' button using the `click()` method.
        8. Wait for a short duration using the `wait()` method.
        9. Assert that the new video source ends with 'ElephantsDream.mp4'.
    """
    audio = ui.video(VIDEO1)
    ui.button('Change source', on_click=lambda: audio.set_source(VIDEO2))

    screen.open('/')
    assert screen.find_by_tag('video').get_attribute('src').endswith('BigBuckBunny.mp4')
    screen.click('Change source')
    screen.wait(0.5)
    assert screen.find_by_tag('video').get_attribute('src').endswith('ElephantsDream.mp4')
