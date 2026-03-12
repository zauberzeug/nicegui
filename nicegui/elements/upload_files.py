import weakref
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path, PurePosixPath

import aiofiles
import anyio
from starlette.datastructures import UploadFile
from starlette.formparsers import MultiPartParser

from .. import json, run


@dataclass
class FileUpload(ABC):
    name: str
    content_type: str

    @abstractmethod
    async def read(self) -> bytes:
        """Read the file contents as bytes."""

    @abstractmethod
    async def text(self, encoding: str = 'utf-8') -> str:
        """Read the file contents as text.

        :param encoding: the encoding to use for the text (default: "utf-8")
        """

    async def json(self, encoding: str = 'utf-8') -> dict:
        """Read the file contents as JSON dictionary.

        :param encoding: the encoding to use for the text (default: "utf-8")
        """
        return json.loads(await self.text(encoding))

    @abstractmethod
    def iterate(self, *, chunk_size: int = 1024 * 1024) -> AsyncIterator[bytes]:
        """Iterate over the file contents as bytes.

        :param chunk_size: the size of each chunk to read in bytes (default: 1 MB)
        """

    @abstractmethod
    async def save(self, path: str | Path) -> None:
        """Save the file contents to a path.

        :param path: the path to save the file contents to
        """

    @abstractmethod
    def size(self) -> int:
        """Get the file size in bytes."""


@dataclass
class SmallFileUpload(FileUpload):
    _data: bytes

    def size(self) -> int:
        return len(self._data)

    async def read(self) -> bytes:
        return self._data

    async def text(self, encoding: str = 'utf-8') -> str:
        return self._data.decode(encoding)

    def iterate(self, *, chunk_size: int = 1024 * 1024) -> AsyncIterator[bytes]:
        async def generator() -> AsyncIterator[bytes]:
            for i in range(0, len(self._data), chunk_size):
                yield self._data[i:i + chunk_size]
        return generator()

    async def save(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        await run.io_bound(target.write_bytes, self._data)


@dataclass
class LargeFileUpload(FileUpload):
    _path: Path

    def __post_init__(self) -> None:
        self._finalizer = weakref.finalize(self, _cleanup_path, self._path)

    def size(self) -> int:
        return self._path.stat().st_size

    async def read(self) -> bytes:
        async with await anyio.open_file(self._path, 'rb') as f:
            return await f.read()

    async def text(self, encoding: str = 'utf-8') -> str:
        data = await self.read()
        return data.decode(encoding)

    def iterate(self, *, chunk_size: int = 1024 * 1024) -> AsyncIterator[bytes]:
        async def generator() -> AsyncIterator[bytes]:
            async with await anyio.open_file(self._path, 'rb') as f:
                while (chunk := await f.read(chunk_size)):
                    yield chunk
        return generator()

    async def save(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        async with await anyio.open_file(target, 'wb') as f:
            async for chunk in self.iterate():
                await f.write(chunk)


def _cleanup_path(path: Path) -> None:
    path.unlink(missing_ok=True)


async def create_file_upload(upload: UploadFile, *, chunk_size: int = 1024 * 1024) -> FileUpload:
    """Create a file upload from a Starlette UploadFile.

    :param upload: the Starlette UploadFile to create a file upload from
    :param chunk_size: the size of each chunk to read in bytes (default: 1 MB)
    """
    memory_limit = (
        getattr(MultiPartParser, 'spool_max_size', 0) or
        getattr(MultiPartParser, 'max_part_size', 0) or  # NOTE: for starlette < 0.46.0
        1024 * 1024
    )

    buffer = BytesIO()
    buffer_size = 0
    temp_file: aiofiles.threadpool.binary.AsyncBufferedIOBase | None = None

    try:
        while (chunk := await upload.read(chunk_size)):
            if not temp_file and buffer_size + len(chunk) > memory_limit:
                temp_file = await aiofiles.tempfile.NamedTemporaryFile('wb', delete=False)
                await temp_file.write(buffer.getvalue())
                buffer = BytesIO()  # release memory
            if not temp_file:
                buffer.write(chunk)
                buffer_size += len(chunk)
            else:
                await temp_file.write(chunk)
    finally:
        await upload.close()
        if temp_file:
            await temp_file.close()

    filename = PurePosixPath(upload.filename or '').name  # strips all path components
    if temp_file:
        return LargeFileUpload(filename, upload.content_type or '', Path(str(temp_file.name)))
    else:
        return SmallFileUpload(filename, upload.content_type or '', buffer.getvalue())
