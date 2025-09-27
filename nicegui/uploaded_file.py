from __future__ import annotations

import asyncio
import os
import tempfile
import weakref
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import anyio
from starlette.formparsers import MultiPartParser


@dataclass
class UploadedFile(ABC):
    name: str
    content_type: str

    @abstractmethod
    async def read(self) -> bytes:
        ...

    @abstractmethod
    async def text(self, encoding: str = 'utf-8') -> str:
        ...

    @abstractmethod
    async def iter_bytes(self, chunk_size: int = 1024 * 1024) -> AsyncIterator[bytes]:
        ...

    @abstractmethod
    async def save(self, path: str | Path) -> Path:
        ...

    @abstractmethod
    def size(self) -> int:
        ...


@dataclass
class SmallUploadedFile(UploadedFile):
    _data: bytes

    def size(self) -> int:
        return len(self._data)

    async def read(self) -> bytes:
        return self._data

    async def text(self, encoding: str = 'utf-8') -> str:
        return self._data.decode(encoding)

    async def iter_bytes(self, chunk_size: int = 1024 * 1024) -> AsyncIterator[bytes]:
        yield self._data

    async def save(self, path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        await asyncio.to_thread(lambda: target.write_bytes(self._data))
        return target


@dataclass
class LargeUploadedFile(UploadedFile):
    _path: Path

    def __post_init__(self) -> None:
        self._finalizer = weakref.finalize(self, _cleanup_path, str(self._path))

    def size(self) -> int:
        return self._path.stat().st_size

    async def read(self) -> bytes:
        async with await anyio.open_file(self._path, 'rb') as f:
            return await f.read()

    async def text(self, encoding: str = 'utf-8') -> str:
        data = await self.read()
        return data.decode(encoding)

    async def iter_bytes(self, chunk_size: int = 1024 * 1024) -> AsyncIterator[bytes]:
        async with await anyio.open_file(self._path, 'rb') as f:
            while True:
                chunk = await f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    async def save(self, path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        async with await anyio.open_file(self._path, 'rb') as f_in, await anyio.open_file(target, 'wb') as f_out:
            while True:
                chunk = await f_in.read(1024 * 1024)
                if not chunk:
                    break
                await f_out.write(chunk)
        return target


def _cleanup_path(path: str) -> None:
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


async def build_uploaded_file_from_upload(upload, *, max_memory_bytes: int | None = None) -> UploadedFile:
    name = getattr(upload, 'filename', '') or ''
    content_type = getattr(upload, 'content_type', '') or ''

    file_obj = getattr(upload, 'file', None)
    if file_obj is None:
        data = b''
        return SmallUploadedFile(name=name, content_type=content_type, _data=data)

    if max_memory_bytes is None:
        max_memory_bytes = int(getattr(MultiPartParser, 'spool_max_size', 1024 * 1024))

    buffer = BytesIO()
    total = 0
    used_temp = False
    tmp_path: Path | None = None
    writer: anyio.AsyncFile | None = None
    chunk_size = 1024 * 1024

    try:
        while True:
            chunk = await upload.read(chunk_size)
            if not chunk:
                break
            if not used_temp:
                buffer.write(chunk)
                total += len(chunk)
                if total > max_memory_bytes:
                    tmp = tempfile.NamedTemporaryFile(delete=False)
                    tmp_path = Path(tmp.name)
                    tmp.close()
                    writer = await anyio.open_file(tmp_path, 'wb')
                    await writer.write(buffer.getvalue())
                    buffer = BytesIO()  # NOTE: release memory by assigning a new instance
                    used_temp = True
            else:
                assert writer is not None
                await writer.write(chunk)
    finally:
        try:
            await upload.close()
        except Exception:
            pass
        if writer is not None:
            await writer.aclose()

    if used_temp and tmp_path is not None:
        return LargeUploadedFile(name=name, content_type=content_type, _path=tmp_path)
    else:
        data = buffer.getvalue()
        return SmallUploadedFile(name=name, content_type=content_type, _data=data)
