import asyncio
import hashlib
import struct
import time
from pathlib import Path


def is_file(path: str | Path | None) -> bool:
    """Check if the path is a file that exists."""
    if not path:
        return False
    if isinstance(path, str) and path.strip().startswith('data:'):
        return False  # avoid passing data URLs to Path
    try:
        return Path(path).is_file()
    except OSError:
        return False


def hash_file_path(path: Path, *, max_time: float | None = None) -> str:
    """Hash the given path based on its string representation and optionally the last modification time of given files."""
    hasher = hashlib.sha256(path.as_posix().encode())
    if max_time is not None:
        hasher.update(struct.pack('!d', max_time))
    return hasher.hexdigest()[:32]


def unlink_with_retry(filepath: Path, *, missing_ok: bool = False, timeout: float = 1.0) -> None:
    """Unlink a file, waiting out transient ``PermissionError`` on Windows.

    A concurrent writer (e.g. a lazily scheduled storage backup) may still hold the file open;
    Windows cannot delete open files, so retry briefly until the handle is released.
    """
    deadline = time.monotonic() + timeout
    while True:
        try:
            filepath.unlink(missing_ok=missing_ok)
            return
        except PermissionError:
            if time.monotonic() > deadline:
                raise
            time.sleep(0.02)


async def unlink_with_retry_async(filepath: Path, *, missing_ok: bool = False, timeout: float = 1.0) -> None:
    """Async variant of :func:`unlink_with_retry` which does not block the event loop while waiting."""
    deadline = time.monotonic() + timeout
    while True:
        try:
            filepath.unlink(missing_ok=missing_ok)
            return
        except PermissionError:
            if time.monotonic() > deadline:
                raise
            await asyncio.sleep(0.02)
