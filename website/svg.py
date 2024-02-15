from pathlib import Path

from nicegui import ui

PATH = Path(__file__).parent / 'static'
HAPPY_FACE_SVG = (PATH / 'happy_face.svg').read_text()
NICEGUI_WORD_SVG = (PATH / 'nicegui_word.svg').read_text()
GITHUB_SVG = (PATH / 'github.svg').read_text()
DISCORD_SVG = (PATH / 'discord.svg').read_text()
REDDIT_SVG = (PATH / 'reddit.svg').read_text()


def face(half: bool = False) -> ui.html:
    """
    Generate an HTML representation of a happy face SVG.

    Args:
        half (bool, optional): If True, only half of the face will be displayed. 
            Defaults to False.

    Returns:
        ui.html: An HTML object containing the SVG code for the happy face.

    Example:
        >>> face()  # Generate a full happy face SVG
        <ui.html object at 0x7f9a8a6b7a90>

        >>> face(half=True)  # Generate a half happy face SVG
        <ui.html object at 0x7f9a8a6b7a90>
    """
    code = HAPPY_FACE_SVG
    if half:
        code = code.replace('viewBox="0 0 62.44 71.74"', 'viewBox="31.22 0 31.22 71.74"')
    return ui.html(code)


def word() -> ui.html:
    """
    Returns an HTML representation of the NICEGUI_WORD_SVG.

    This function generates an HTML representation of the NICEGUI_WORD_SVG,
    which can be used to display the SVG image on a web page.

    Returns:
        ui.html: An HTML object containing the SVG image.

    Example:
        svg = word()
        print(svg)  # <ui.html object at 0x12345678>
    """
    return ui.html(NICEGUI_WORD_SVG)


def github() -> ui.html:
    """
    Returns an HTML object containing the SVG code for the GitHub logo.

    This function is used to generate an HTML object that represents the SVG code for the GitHub logo.
    The returned HTML object can be used to embed the GitHub logo in a web page.

    Returns:
        ui.html: An HTML object containing the SVG code for the GitHub logo.
    """
    return ui.html(GITHUB_SVG)


def discord() -> ui.html:
    """
    Returns an HTML object containing the Discord SVG.

    This function returns an instance of the `ui.html` class that represents an HTML object containing the Discord SVG.
    The SVG is retrieved from the `DISCORD_SVG` constant.

    Returns:
        ui.html: An HTML object containing the Discord SVG.

    Example:
        svg = discord()
        # Use the `svg` object to display the Discord SVG on a webpage.
    """
    return ui.html(DISCORD_SVG)


def reddit() -> ui.html:
    """
    Returns an HTML object containing the SVG representation of the Reddit logo.

    This function retrieves the SVG data for the Reddit logo and wraps it in an
    `ui.html` object. The resulting HTML can be used to display the Reddit logo
    on a web page.

    Returns:
        ui.html: An HTML object containing the SVG representation of the Reddit logo.
    """
    return ui.html(REDDIT_SVG)
