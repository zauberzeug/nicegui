from pathlib import Path
from typing import Optional, Union

from .. import core, helpers
from ..context import context


class Download:
    """Download functions

    These functions allow you to download files, URLs or raw data.

    *Added in version 2.14.0*
    """

    def __call__(self, src: Union[str, Path, bytes], filename: Optional[str] = None, media_type: str = '') -> None:
        """Download

        Function to trigger the download of a file, URL or bytes.

        :param src: target URL, local path of a file or raw data which should be downloaded
        :param filename: name of the file to download (default: name of the file on the server)
        :param media_type: media type of the file to download (default: "")
        """
        if isinstance(src, bytes):
            self.content(src, filename, media_type)
        elif helpers.is_file(src):
            self.file(src, filename, media_type)
        else:
            src = str(src)
            self.from_url(src, filename, media_type)

    def file(self, path: Union[str, Path], filename: Optional[str] = None, media_type: str = '') -> None:
        """Download file from local path

        Function to trigger the download of a file.

        *Added in version 2.14.0*

        :param path: local path of the file
        :param filename: name of the file to download (default: name of the file on the server)
        :param media_type: media type of the file to download (default: "")
        """
        src = core.app.add_static_file(local_file=path, single_use=True)
        context.client.download(src, filename, media_type)

    def from_url(self, url: str, filename: Optional[str] = None, media_type: str = '') -> None:
        """Download from a URL

        Function to trigger the download from a URL.

        *Added in version 2.14.0*

        :param url: URL
        :param filename: name of the file to download (default: name of the file on the server)
        :param media_type: media type of the file to download (default: "")
        """
        context.client.download(url, filename, media_type)

    def content(self, content: Union[bytes, str], filename: Optional[str] = None, media_type: str = '') -> None:
        """Download raw bytes or string content

        Function to trigger the download of raw data.

        *Added in version 2.14.0*

        :param content: raw bytes or string
        :param filename: name of the file to download (default: name of the file on the server)
        :param media_type: media type of the file to download (default: "")
        """
        if isinstance(content, str):
            content = content.encode('utf-8')
        context.client.download(content, filename, media_type)


download = Download()
