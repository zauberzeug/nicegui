from pathlib import Path
from typing import Optional, Union

from .. import context, core, helpers


def download(src: Union[str, Path], filename: Optional[str] = None) -> None:
    """Download

    Function to trigger the download of a file.

    :param src: target URL or local path of the file which should be downloaded
    :param filename: name of the file to download (default: name of the file on the server)
    """
    if helpers.is_file(src):
        src = core.app.add_static_file(local_file=src, single_use=True)
    else:
        src = str(src)
    context.get_client().download(src, filename)
