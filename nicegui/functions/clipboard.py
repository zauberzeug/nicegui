from .javascript import run_javascript


def read():
    """
    Read the data from the clipboard.
    """

    return run_javascript('navigator.clipboard.read()')


def readText():
    """
    Reads the text from the clipboard.

    Returns:
        str: The text from the clipboard.
    """
    return run_javascript('navigator.clipboard.readText()')


def write(data):
    """
    Writes the specified data to the clipboard.

    Parameters:
        data: The data to be written to the clipboard.
    """
    run_javascript(f'navigator.clipboard.write(`{data}`)')


def writeText(text):
    """
    Writes the specified text to the clipboard.

    Parameters:
        text (str): The text to be written to the clipboard.

    Example:
    >>> ui.clipboard.writeText("Hello, world!")
    """
    run_javascript(f'navigator.clipboard.writeText(`{text}`)')
