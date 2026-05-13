from pathlib import Path

from .. import core, helpers
from ..context import context
from ..logging import log


class Download:
    """Download functions

    These functions allow you to download files, URLs or raw data.

    *Added in version 2.14.0*
    """

    def __call__(self, src: str | Path | bytes, filename: str | None = None, media_type: str = '') -> None:
        """Download

        Function to trigger the download of a file, URL or bytes.

        :param src: relative target URL, local path of a file or raw data which should be downloaded
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

    def file(self, path: str | Path, filename: str | None = None, media_type: str = '') -> None:
        """Download file from local path

        Function to trigger the download of a file.

        *Added in version 2.14.0*

        :param path: local path of the file
        :param filename: name of the file to download (default: name of the file on the server)
        :param media_type: media type of the file to download (default: "")
        """
        src = core.app.add_static_file(local_file=path, single_use=True)
        context.client.download(src, filename, media_type)

    def from_url(self, url: str, filename: str | None = None, media_type: str = '') -> None:
        """Download from a relative URL

        Function to trigger the download from a relative URL.

        Note:
        This function is intended to be used with relative URLs only.
        For absolute URLs, the browser ignores the download instruction and tries to view the file in a new tab
        if possible, such as images, PDFs, etc.
        Therefore, the download may only work for some file types such as .zip, .db, etc.
        Furthermore, the browser ignores filename and media_type parameters,
        respecting the origin server's headers instead.
        Either replace the absolute URL with a relative one, or use ``ui.navigate.to(url, new_tab=True)`` instead.

        *Added in version 2.14.0*

        *Updated in version 2.19.0: Added warning for cross-origin downloads*

        :param url: URL
        :param filename: name of the file to download (default: name of the file on the server)
        :param media_type: media type of the file to download (default: "")
        """
        is_relative = url.startswith('/') or url.startswith('./') or url.startswith('../')
        if not is_relative:
            log.warning('Using `ui.download.from_url` with absolute URLs is not recommended.\n'
                        'Please refer to the documentation for more details.')
        context.client.download(url, filename, media_type)

    def content(self, content: bytes | str, filename: str | None = None, media_type: str = '') -> None:
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
