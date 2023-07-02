from pathlib import Path
from typing import Optional, Union

from .. import globals


def download(src: Union[str, Path], filename: Optional[str] = None) -> None:
    """Download

    Function to trigger the download of a file.

    :param src: target URL or local filename which should be downloaded
    :param filename: name of the file to download (default: name of the file on the server)
    """
    if Path(src).is_file():
        src = globals.app.add_static_file(local_file=src)
    globals.get_client().download(src, filename)
