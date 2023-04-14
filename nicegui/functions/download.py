from typing import Optional

from .. import globals


def download(url: str, filename: Optional[str] = None) -> None:
    """Download

    Function to trigger the download of a file.

    :param url: target URL of the file to download
    :param filename: name of the file to download (default: name of the file on the server)
    """
    globals.get_client().download(url, filename)
